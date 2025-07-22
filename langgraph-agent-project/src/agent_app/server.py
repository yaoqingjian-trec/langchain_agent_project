# src/agent_app/server.py

import os
import asyncio
import json
from fastapi import FastAPI, Query
# --- 1. 导入CORS中间件 ---
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# --- 初始化与引导 ---
load_dotenv()
from .agent import build_agent_graph

print("正在构建并编译LangGraph应用...")
app_graph = build_agent_graph()
print("LangGraph应用已准备就绪。")

api = FastAPI(
    title="LangGraph Research Agent API",
    description="一个通过API接口暴露的智能研究助理",
    version="1.0.0",
)

# --- 2. 配置CORS中间件 ---
# 这是解决CORS错误的关键部分
origins = [
    "*",  # 在开发环境中，使用"*"允许所有来源，最简单
    # "http://localhost",
    # "http://localhost:3000", # 如果您有React/Vue等前端应用，将来可以写具体的地址
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 允许所有HTTP方法
    allow_headers=["*"], # 允许所有HTTP请求头
)


# --- 3. 定义数据模型 ---
class QuestionRequest(BaseModel):
    question: str

# --- 4. 定义 API 端点 (这部分完全无需修改) ---

@api.get("/")
def read_root():
    return {"status": "LangGraph Agent API is running."}


@api.api_route("/stream", methods=["POST", "GET"])
async def stream_agent(request: QuestionRequest = None, question: str = Query(None)):
    """
    流式调用智能体，实时返回每一步的输出，包括LLM的思考和工具的使用。
    """
    if request and request.question:
        user_question = request.question
    elif question:
        user_question = question
    else:
        return {"error": "Question not provided"}, 400

    inputs = {"messages": [HumanMessage(content=user_question)]}

    async def event_generator():
        try:
            async for event in app_graph.astream_events(inputs, version="v2"):
                kind = event["event"]
                
                if kind == "on_tool_start":
                    sse_data = { "type": "tool_start", "node": event["name"], "input": event["data"].get("input") }
                    yield {"event": "agent_step", "data": json.dumps(sse_data)}

                elif kind == "on_tool_end":
                    sse_data = { "type": "tool_end", "node": event["name"], "output_preview": str(event["data"].get("output"))[:100] + "..." }
                    yield {"event": "agent_step", "data": json.dumps(sse_data)}

                elif kind == "on_chat_model_stream":
                    chunk = event["data"].get("chunk")
                    if chunk and hasattr(chunk, 'content') and chunk.content:
                        sse_data = { "type": "llm_chunk", "node": event["name"], "content": chunk.content }
                        yield {"event": "agent_step", "data": json.dumps(sse_data)}
            
            yield {"event": "end", "data": "Stream ended"}

        except asyncio.CancelledError:
            print("客户端断开连接，停止流式传输。")
        except Exception as e:
            print(f"流式传输中发生错误: {e}")
            yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_generator())