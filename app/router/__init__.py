from fastapi import APIRouter, WebSocket
from fastapi.responses import StreamingResponse

from lib.templates import templates
from service import gemini_consulting

router = APIRouter(
    prefix="/chat"
)

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
# 대화 히스토리를 저장할 딕셔너리 (추후 DB로 변경 예정)
chat_sessions = {}

@router.get("/ws")
async def get_chat_websocket():
    return templates.TemplateResponse("chat_socket.html", {"request": {}})

@router.websocket("/ws/response/{session_id}")
async def websocket_chat_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    # 세션별로 대화 시작
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_session = chat_sessions[session_id]




# @router.get("/ws")
# async def chat_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     chat = client.chat.create

#     try:
#     except WebSocketDisconnect:
#         print("WebSocket disconnected")
#     except Exception as e:
#         print(f"Error: {e}")

#     pass