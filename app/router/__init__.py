from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from lib.templates import templates

router = APIRouter()

"""
컨설팅 html 마크업
"""
@router.get("/chat")
async def get_chat_html():
    return templates.TemplateResponse("chat.html", {"request": {}})

@router.get("/ws")
async def chat_endpoint(websocket: WebSocket):
    pass