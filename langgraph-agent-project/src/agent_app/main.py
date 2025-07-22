# langgraph-agent-project/src/agent_app/main.py

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# --- 把 load_dotenv() 移动到这里！ ---
# 在所有其他导入之前加载环境变量，确保它们在任何模块初始化时都可用。
load_dotenv()

# 现在再导入我们自己的模块，这时 agent.py 已经可以访问到环境变量了
from .agent import build_agent_graph

def main():
    """
    运行智能体的主函数。
    """
    # 检查密钥是否已设置（现在它们应该已经被加载了）
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("错误: 未设置 OpenAI 或 Tavily 的 API 密钥。")
        print("请检查您的 .env 文件并确保填入了正确的密钥。")
        return

    # 在 main 函数开始时构建 app
    print("正在构建智能体图...")
    app = build_agent_graph()
    
    print("\nLangGraph 智能研究助理已就绪。")
    print("输入 'exit' 退出程序。")

    while True:
        user_input = input("\n请输入您的问题: ")
        if user_input.lower() == 'exit':
            break

        if not user_input.strip():
            continue

        inputs = {"messages": [HumanMessage(content=user_input)]}
        
        print("\n--- 智能体正在思考中... ---\n")
        
        for event in app.stream(inputs, stream_mode="values"):
            last_message = event["messages"][-1]
            if last_message.name == "tool_output":
                print("--- 工具输出 ---")
                print(last_message.content)
            else:
                print(f"--- LLM 响应 ({last_message.type}) ---")
                print(last_message.content)
            print("\n" + "="*30 + "\n")

if __name__ == "__main__":
    main()