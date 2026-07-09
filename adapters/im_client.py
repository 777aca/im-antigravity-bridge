import httpx

class IMClient:
    def __init__(self, platform: str, webhook_url: str):
        self.platform = platform
        self.webhook_url = webhook_url

    async def send_message(self, user_id: str, content: str):
        # 通用的伪代码实现，可根据具体的飞书/钉钉 API 进行替换
        payload = {
            "msg_type": "text",
            "content": {
                "text": content
            },
            "user_id": user_id
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()
                return True
            except httpx.HTTPError:
                return False
