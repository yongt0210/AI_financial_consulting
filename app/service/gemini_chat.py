import json

from fastapi import  WebSocket
from google.genai import types

from lib.gemini import genai_client as client
from lib.prompt import SYSTEM_INSTRUCTION

class GeminiConsulting:
    def __init__(self):
        self.client = client
        self.model = "gemini-2.5-flash"

        # 세션 관리를 위한 딕셔너리(추후 DB로 변경 예정)
        self.sessions = {}

    async def ai_finance_consulting(self, question: str):
        """
        AI 금융 컨설팅 서비스(eventStream용)
        """
        try:
            response = await self.client.aio.models.generate_content_stream(
                model=self.model,
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

    async def get_session(self, session_id: str):
        """
        채팅용 세션 호출
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = self.client.aio.chats.create(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION
                )
            )
        return self.sessions[session_id]

    async def generate_chat_response(self, session_id: str, question: str):
        """
        채팅용 응답 생성
        """

        chat_session = await self.get_session(session_id)

        print(dir(chat_session))

        async for chunk in await chat_session.send_message_stream(question):
            if chunk.text:
                yield chunk.text


gemini_consulting = GeminiConsulting()