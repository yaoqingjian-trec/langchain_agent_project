import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub # 确保导入 hub

# --- 1. 从.env文件加载环境变量 ---
load_dotenv()

# 检查环境变量
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("Tavily API Key not found. Please set it in your .env file.")
if not os.getenv("SILICONFLOW_API_KEY"):
    raise ValueError("SiliconFlow API Key not found. Please set it in your .env file.")

# --- 2. 定义智能体的组件 ---

# a) 大脑 (LLM)
print("正在初始化大脑，使用硅基流动的 Qwen/Qwen3-14B 模型...")
llm = ChatOpenAI(
    model="Qwen/Qwen3-14B",
    # model="moonshotai/Kimi-K2-Instruct", # 解析出错
    temperature=0,
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)
print("大脑初始化完成！")

# b) 工具 (Tools)
print("正在初始化工具...")
tools = [TavilySearch(max_results=2)]
print("工具初始化完成！")

# c) 提示/指令 (Prompt) - 切换为 ReAct 模式
print("正在从 LangChain Hub 加载 ReAct 提示...")
prompt = hub.pull("hwchase17/react-chat")
print("提示加载完成！")

# --- 3. 组装并运行智能体 ---
print("正在组装 ReAct 智能体...")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
print("智能体组装完成！")

# --- 4. 让智能体开始工作！ ---
print("\n智能体已准备就绪，请输入你的问题...")
response = agent_executor.invoke({
    "input": "现在北京和伦敦的时间分别是几点？它们之间差了几个小时？",
    "chat_history": []  # <-- 已添加此行来修复 KeyError
})

print("\n--- 最终答案 ---")
print(response["output"])