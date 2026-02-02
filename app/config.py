import os

# 구글 API 키를 환경변수에서 호출
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Redis 접속 정보 설정
REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST"),
    "port": int(os.getenv("REDIS_PORT", 6379)),
    "db": int(os.getenv("REDIS_DB", 0)),
    "password": os.getenv("REDIS_PASS")
}