# langgraph-agent-project/src/agent_app/agent.py

import os
import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_litellm import ChatLiteLLM # <--- 修改为从新包导入
from langgraph.graph import StateGraph, END
import io

from langchain_tavily import TavilySearch

# --- 1. 定义智能体的状态 ---
class AgentState(TypedDict):
    """
    代表我们智能体的状态。
    """
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. 定义工具和LLM (使用 ChatLiteLLM 连接硅基流动) ---
tool = TavilySearch(max_results=2)

# 使用 ChatLiteLLM 来调用硅基流动的 API
# 它会从环境变量中读取配置
model = ChatLiteLLM(
    model=os.getenv("SILICONFLOW_MODEL_NAME"),
    api_base=os.getenv("SILICONFLOW_API_BASE"),
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    # 告诉 LiteLLM 硅基流动的 API 格式与 OpenAI 兼容，这很关键
    custom_llm_provider="openai",
    temperature=0,
)

# --- 3. 定义图的节点 ---

def route_question(state: AgentState) -> dict:
    """
    分析用户问题，并将其决策作为一条消息添加到状态中。
    """
    print("--- 节点: 路由问题 ---")
    messages = state['messages']
    last_message = messages[-1]

    prompt = f"""
    你是一个智能路由器。根据用户的以下问题，判断是否需要通过网络搜索来获取额外信息才能回答。
    用户问题: "{last_message.content}"

    如果问题是简单的问候、计算、或者不需要外部知识的常识性问题，请回答 'generate'。
    如果问题需要获取最新的新闻、具体事实、或任何外部信息，请回答 'continue'。
    """
    
    response = model.invoke([HumanMessage(content=prompt)])
    decision = response.content
    print(f"路由决策: {decision}")

    # 将决策结果作为一个特殊的消息存入状态，以便后续的条件边读取
    return {"messages": [HumanMessage(content=decision, name="routing_decision")]}


def call_tool(state: AgentState) -> dict:
    """
    调用搜索工具。
    """
    print("--- 节点: 调用工具 ---")
    # 找到最后一个非决策消息来进行搜索
    query = ""
    for msg in reversed(state['messages']):
        if msg.name not in ("routing_decision", "tool_output"):
            query = msg.content
            break
    
    if not query:
        # 如果找不到合适的查询，返回一个错误信息
        return {"messages": [HumanMessage(content="无法确定要搜索的内容。", name="tool_output")]}

    print(f"正在使用查询进行搜索: '{query}'")
    action_result = tool.invoke(query)
    return {"messages": [HumanMessage(content=str(action_result), name="tool_output")]}

def should_continue(state: AgentState) -> str:
    """
    判断在搜索后是否需要继续或重写查询。
    """
    print("--- 节点: 判断是否继续? ---")
    last_message = state['messages'][-1]
    
    original_question = ""
    for msg in state['messages']:
        if msg.type == "human" and msg.name is None:
            original_question = msg.content
            break

    prompt_template = f"""
    原始问题: '{original_question}'
    
    根据以下搜索结果，判断是否已经有足够的信息来回答原始问题。
    搜索结果:
    {last_message.content}

    如果信息足够，请回答 'generate'。
    如果信息不足，请回答 'rewrite'。
    """
    
    response = model.invoke([HumanMessage(content=prompt_template)])
    decision = response.content
    print(f"来自LLM的决策: {decision}")

    if "generate" in decision.lower():
        return "generate"
    else:
        return "rewrite"

def generate_answer(state: AgentState) -> dict:
    """
    为用户生成最终答案。
    """
    print("--- 节点: 生成最终答案 ---")
    # 为了更好的回答，我们可以让LLM忽略掉我们的内部决策消息
    final_messages = [msg for msg in state['messages'] if msg.name not in ("routing_decision",)]
    
    response = model.invoke(final_messages + [HumanMessage(content="请根据我们的对话内容，为用户的初始问题提供一个全面的、友好的答案。")])
    return {"messages": [response]}

def rewrite_query(state: AgentState) -> dict:
    """
    根据LLM的建议重写搜索查询。
    """
    print("--- 节点: 重写查询 ---")
    prompt = f"""
    根据以下对话，新的、优化后的搜索查询建议是什么？
    只返回搜索查询本身，不要添加任何其他内容。

    对话内容:
    {[msg.pretty_repr() for msg in state['messages']]}
    """
    response = model.invoke([HumanMessage(content=prompt)])
    print(f"新的查询: {response.content}")
    return {"messages": [HumanMessage(content=response.content)]}

# --- 4. 构建并编译图 ---

def build_agent_graph():
    """
    构建 LangGraph 智能体。
    """
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("router", route_question)
    graph_builder.add_node("agent", call_tool)
    graph_builder.add_node("rewriter", rewrite_query)
    graph_builder.add_node("generator", generate_answer)
    
    graph_builder.set_entry_point("router")

    # 定义从路由器出发的条件边逻辑
    def route_logic(state: AgentState) -> str:
        last_message = state['messages'][-1]
        if last_message.name == "routing_decision":
            if "generate" in last_message.content.lower():
                return "generate"
        return "continue"

    graph_builder.add_conditional_edges("router", route_logic, {"generate": "generator", "continue": "agent"})
    
    # 定义从agent(工具调用)出发的条件边
    graph_builder.add_conditional_edges("agent", should_continue, {"rewrite": "rewriter", "generate": "generator"})
    
    graph_builder.add_edge("rewriter", "agent")
    graph_builder.add_edge("generator", END)

    app = graph_builder.compile()

    try:
        from PIL import Image
        image_bytes = app.get_graph().draw_mermaid_png()
        image = Image.open(io.BytesIO(image_bytes))
        image.save("agent_graph.png")
        print("智能体流程图已保存为 agent_graph.png")
    except Exception as e:
        print(f"提示：无法生成可视化流程图，因为缺少依赖。错误信息: {e}")
        print("要启用此功能，请先在系统中安装 Graphviz，然后运行: uv pip install -e \".[viz]\"")

    return app