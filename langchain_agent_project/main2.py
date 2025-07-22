# main.py (使用 gpt-3.5-turbo-0125 模型)

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- 1. 从.env文件加载环境变量 ---
load_dotenv()

# 检查Tavily API Key是否已设置
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("Tavily API Key not found. Please set it in your .env file.")

# 检查SiliconFlow API Key是否已设置
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI API Key not found. Please set it in your .env file.")

# --- 2. 定义智能体的组件 ---

# a) 大脑 (LLM) - 已切换到 Qwen3-32B
print("正在初始化大脑，使用硅基流动的 Qwen/Qwen3-32B 模型...")
# llm = ChatOpenAI(
#     # model="Qwen/Qwen3-32B",  # 不能主动调用tool
#     # model="Qwen/QwQ-32B",    # 不能主动调用tool
#     # model="deepseek-ai/DeepSeek-R1", # 一直没反应，好像卡死了的状态
#     # model="moonshotai/Kimi-K2-Instruct", # 不能主动调用tool
#     # model="baidu/ERNIE-4.5-300B-A47B", # 不能主动调用tool
#     temperature=0,
#     api_key=os.getenv("SILICONFLOW_API_KEY"),
#     base_url="https://api.siliconflow.cn/v1"
# )
llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",  # openAI的模型可以调用tool，硅基流动的模型不能主动调用tool
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)
print("大脑初始化完成！")

# b) 工具 (Tools) - 使用新的、独立的包
print("正在初始化工具...")
tools = [TavilySearch(max_results=2)]
print("工具初始化完成！")

# c) 提示/指令 (Prompt)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can search the web."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# --- 3. 组装并运行智能体 ---
print("正在组装智能体...")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
print("智能体组装完成！")

# --- 4. 让智能体开始工作！ ---
print("\n智能体已准备就绪，请输入你的问题...")
response = agent_executor.invoke({
    "input": "现在北京和伦敦的时间分别是几点？它们之间差了几个小时？"
})

print("\n--- 最终答案 ---")
<<<<<<< HEAD
print(response["output"])
=======
print(response["output"])
>>>>>>> d7531dfec609941de283ff4435a2a18cf2ada245
