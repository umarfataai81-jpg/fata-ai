import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Bamu samu GEMINI_API_KEY ba!")

client = genai.Client(api_key=api_key)
app = FastAPI(title="Fata AI Engine", description="Babban AI Gateway na Fata AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str = "guest"
    message: str

@app.get("/")
def home():
    return {"status": "Active", "system": "Fata AI Engine yana aiki lafiya!"}

@app.post("/v1/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Sakon wayam ne.")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=request.message,
        )
        return {"status": "success", "app": "Fata AI", "user_id": request.user_id, "response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
