import json
import uuid
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import StreamingResponse

from lib.templates import templates
from service import gemini_consulting

from config import survey_list
from schema import assetData

router = APIRouter(
    prefix="/chat"
)

"""
DC형 퇴직연금
"""
@router.get("/dc")
async def get_dc_consult(request: Request):
    return templates.TemplateResponse(
        "dc.html",
        {
            "request": request,
            "survey_list": survey_list      # 3. Jinja2에서 루프를 돌릴 데이터를 최상단 키로 전달
        }
    )

@router.post("/dc/data")
async def get_dc_consult_data(
    data: assetData,
):
    return await gemini_consulting.ai_dc_pension_consulting(data=data)

"""
컨설팅 eventStream
"""
@router.get("/eventstream")
async def get_chat_html():
    return templates.TemplateResponse("chat.html", {"request": {}})

@router.get("/eventstream/response")
async def get_chat_response(question: str):
    return StreamingResponse(
        gemini_consulting.ai_finance_consulting(question),
        media_type="text/event-stream"
    )

"""
컨설팅 WebSocket
"""
@router.get("/ws")
async def get_chat_websocket():
    return templates.TemplateResponse("chat_socket.html", {"request": {}, "session_id": str(uuid.uuid4())})

@router.websocket("/ws/response/{session_id}")
async def websocket_chat_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    try:
        while True:
            question = await websocket.receive_text()

            async for text_chunk in gemini_consulting.generate_chat_response(session_id, question=question):
                await websocket.send_json({
                    "type": "stream",
                    "text": text_chunk
                })

            await websocket.send_json({
                "type": "end",
                "text": "Connection closed"
            })
    except WebSocketDisconnect:
        print("웹소켓 종료")
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "text": f"{str(e)}\n{traceback.format_exc()}"
        })