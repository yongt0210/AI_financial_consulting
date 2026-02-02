import asyncio
from collections import defaultdict

from fastapi import WebSocket
from starlette.websockets import WebSocketState

from lib.redis import redis_client
from lib.logger import get_logger

logger = get_logger()

# 웹소켓 연결 관리 클래스
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, service: str):
        await websocket.accept()
        self.active_connections[service].append(websocket)

    def disconnect(self, websocket: WebSocket, service: str):
        if service in self.active_connections:
            if websocket in self.active_connections[service]:
                self.active_connections[service].remove(websocket)

    async def broadcast(self, service: str, message: str):
        # 해당 서비스(채팅방)에 있는 모든 소켓에게 전송
        connections = self.active_connections.get(service, [])

        if not connections:
            return

        # 웹소켓 전송 병렬 실행
        # 죽은 소켓에 보내는 것은 무시(return_exceptions=True)
        tasks = [
            connection.send_text(message)
            for connection in connections
            if connection.client_state == WebSocketState.CONNECTED
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

manager = ConnectionManager()

# 전역 Redis pubsub 리스너: 서버당 1개만 실행되어 Redis 메시지를 수신 후 Manager로 전달
async def global_redis_listener():
    """
    모든 채팅 채널의 메시지를 구독하고, 적절한 서비스(방)로 라우팅합니다.
    패턴 구독(psubscribe)을 사용합니다.
    """
    pubsub = redis_client.client.pubsub()

    # 'service:'로 시작하는 모든 채널 구독
    await pubsub.psubscribe("service:*")

    try:
        async for message in pubsub.listen():
            if message["type"] == "pmessage": # 패턴 매칭 메시지는 pmessage 타입
                channel = message["channel"] # 예: service:test:chat
                data = message["data"]

                # 채널명에서 service 이름 추출 로직
                parts = channel.split(":")
                if len(parts) >= 2:
                    service_name = parts[1] # 'test' 추출

                    # 메모리에 연결된 여러 클라이언트에게 브로드캐스팅
                    await manager.broadcast(service_name, data)

    except asyncio.CancelledError:
        logger.info("Global Redis Listener 종료 중...")
    except Exception as e:
        logger.error(f"Global Redis Listener 에러: {repr(e)}")
    finally:
        await pubsub.close()
