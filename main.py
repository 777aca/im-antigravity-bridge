import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from services.agent_runner import agent_runner
from adapters.feishu_client import FeishuClient

# 加载环境变量
load_dotenv()

app = FastAPI(title="IM Antigravity Bridge - Feishu")

# 初始化飞书客户端
feishu_client = FeishuClient()

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    
    # 1. 飞书 URL 校验 (Challenge)
    if "challenge" in data and data.get("type") == "url_verification":
        return {"challenge": data["challenge"]}
    
    # 2. 解析飞书消息事件 (schema 2.0)
    # 此处假设用户发送的是纯文本，且只处理 im.message.receive_v1
    header = data.get("header", {})
    if header.get("event_type") == "im.message.receive_v1":
        event = data.get("event", {})
        sender = event.get("sender", {}).get("sender_id", {})
        # 默认优先取 open_id
        user_id = sender.get("open_id", "")
        
        message = event.get("message", {})
        msg_type = message.get("msg_type", "")
        
        if msg_type != "text":
            return {"status": "ignored", "reason": "only text messages are supported"}
            
        content_str = message.get("content", "{}")
        try:
            content_dict = json.loads(content_str)
            command_text = content_dict.get("text", "")
        except json.JSONDecodeError:
            command_text = ""
            
        if not command_text:
            return {"status": "ignored", "reason": "empty text"}
            
        # 去除可能包含的 @ 机器人部分 (简化处理，如果有)
        command_text = command_text.replace("@_user_1", "").strip()

        # 调用 Antigravity Agent 执行指令
        try:
            agent_reply = await agent_runner.process_message(command_text)
            # 将 Agent 响应回传至飞书
            await feishu_client.send_message(user_id=user_id, content=agent_reply)
            return {"status": "success"}
        except Exception as e:
            error_msg = f"Agent execution failed: {str(e)}"
            await feishu_client.send_message(user_id=user_id, content=error_msg)
            return {"status": "error", "detail": error_msg}

    return {"status": "ignored", "reason": "unhandled event type"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
