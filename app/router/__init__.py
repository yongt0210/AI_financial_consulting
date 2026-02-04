from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from lib.templates import templates
from service import ai_finance_consulting

router = APIRouter()

"""
컨설팅 html 마크업
"""
@router.get("/chat")
async def get_chat_html():
    return templates.TemplateResponse("chat.html", {"request": {}})

@router.get("/chat/response")
async def get_chat_response(question: str):
    return StreamingResponse(
        ai_finance_consulting(question),
        media_type="text/event-stream"
    )


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