# 파이썬 3.13
FROM python:3.13.1-slim-bookworm

# 작업 디렉토리 설정
WORKDIR /app

# 파이썬 의존성 설치
COPY requirements.txt .
RUN pip install -r requirements.txt
