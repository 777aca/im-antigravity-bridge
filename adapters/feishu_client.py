import os
import lark_oapi as lark
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody

class FeishuClient:
    def __init__(self):
        self.app_id = os.getenv("FEISHU_APP_ID", "")
        self.app_secret = os.getenv("FEISHU_APP_SECRET", "")
        
        # 初始化客户端
        self.client = lark.Client.builder() \
            .app_id(self.app_id) \
            .app_secret(self.app_secret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()

    async def send_message(self, user_id: str, content: str) -> bool:
        """
        向指定用户发送飞书消息
        user_id_type 支持 open_id, user_id, union_id 甚至 chat_id (发群消息)
        """
        try:
            request: CreateMessageRequest = CreateMessageRequest.builder() \
                .receive_id_type("open_id") \
                .request_body(CreateMessageRequestBody.builder()
                    .receive_id(user_id)
                    .msg_type("text")
                    .content(f'{{"text":"{content}"}}')
                    .build()) \
                .build()

            # 发起API调用 (注意：lark-oapi 最新版本支持协程，如果不支持则使用同步)
            # 根据官方文档 client.im.v1.message.create() 是同步方法，这里包一层
            response = self.client.im.v1.message.create(request)

            if not response.success():
                print(f"Feishu send_message error: {response.code} - {response.msg}, log_id: {response.get_log_id()}")
                return False
            return True
        except Exception as e:
            print(f"Feishu send_message exception: {str(e)}")
            return False
