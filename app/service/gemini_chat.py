import json

from fastapi import  WebSocket
from google.genai import types

from lib.gemini import genai_client as client
from lib.prompt import SYSTEM_INSTRUCTION

model = 'gemini-2.5-flash'

class GeminiConsulting:
    def __init__(self):
        self.client = client
        self.model = "gemini-2.5-flash"
        self.sessions = {}

    async def ai_finance_consulting(self, question: str):
        """
        AI 금융 컨설팅 서비스(eventStream용)
        """
        try:
            response = await client.aio.models.generate_content_stream(
                model=model,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7, # 창의성 조절
                )
            )
            # 비동기 반복문으로 청크(chunk) 단위 수신
            async for chunk in response:
                if chunk.text:
                    data_content = json.dumps({"text": chunk.text}, ensure_ascii=False)

                    yield "event: stream\n"
                    yield f"data: {data_content}\n\n"

            yield "event: end\ndata: {'text': 'Connection closed'}\n\n"
        except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"

    async def websocket_ai_finance_consulting(self, websocket: WebSocket, question: str):
        """
        AI 금융 컨설팅 서비스(웹소켓용)
        """
        pass

gemini_consulting = GeminiConsulting()