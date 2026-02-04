import json
from google.genai import types

from lib.gemini import genai_client as client
from lib.prompt import SYSTEM_INSTRUCTION

async def ai_finance_consulting(question: str):
    """
    AI 금융 컨설팅 서비스
    """

    try:
        response = await client.aio.models.generate_content_stream(
            model='gemini-2.5-flash',
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
