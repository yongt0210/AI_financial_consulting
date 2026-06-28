import json

from fastapi import WebSocket
from google.genai import types

from lib.gemini import genai_client as client
from lib.prompt import CONSULT_INSTRUCTION, PENSION_INSTRUCTION

from config import survey_list
from schema import assetData, portfolioResult

class GeminiConsulting:
    def __init__(self):
        self.client = client
        self.model = "gemini-2.5-flash-lite"

        # 세션 관리를 위한 딕셔너리(추후 DB로 변경 예정)
        self.sessions = {}

    # DC형 퇴직연금 상담 결과
    async def ai_dc_pension_consulting(self, data: assetData):
        result = {
            "code": 200
            , "result": {}
        }

        try:
            # 기본정보
            base_info = data.base
            answer = f"""
# 기본정보
## 나이: {base_info.age}세
## 성별: {base_info.sex}
## 총 자산: {base_info.wealth}
## 소득: {base_info.income}
"""
            # 퇴직연금
            answer_list = data.answers

            for i, survey in enumerate(survey_list):
                answer += f"""
# 카테고리: {survey.get('category')}"""

                question_list = survey.get("list")

                for j, question in enumerate(question_list):
                    q = question.get("question")
                    a_int = answer_list[i][j]
                    a = question.get("answer")[a_int]

                    answer += f"""
## 질문{j+1}: {q}
## 응답{j+1}: {a}
"""
                answer += """
            """

            # 기타
            if data.etc:
                answer += f"""
# 그 외 하고싶은 말: {data.etc}
"""

            prompt = f"""
아래 질의응답문을 토대로 퇴직연금 포트폴리오를 추천해주세요.
{answer}
"""

            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=PENSION_INSTRUCTION,
                    temperature=0.4, # 창의성 조절
                    response_mime_type="application/json",
                    response_schema=portfolioResult,
                )
            )

            result["result"] = json.loads(response.text)
        except Exception as e:
            result = {
                "code": 500,
                "error": str(e)
            }

        return result

    async def ai_finance_consulting(self, question: str):
        """
        AI 금융 컨설팅 서비스(eventStream용)
        """
        try:
            response = await self.client.aio.models.generate_content_stream(
                model=self.model,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=CONSULT_INSTRUCTION,
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
                    system_instruction=CONSULT_INSTRUCTION
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