from fastapi import FastAPI

app = FastAPI(
    title="AI 재무 컨설팅 서비스",
    summary="AI 재무 컨설팅 서비스",
    version="1.0.0",
)

@app.get(
    "/",
    name="index",
    summary="헬스 체크",
    description="헬스 체크",
    tags=["main"],
)
def get_health_check() -> str:
    return "health check"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)