from google import genai
from config import GOOGLE_API_KEY

# Gemini 클라이언트 설정
genai_client = genai.Client(api_key=GOOGLE_API_KEY)
