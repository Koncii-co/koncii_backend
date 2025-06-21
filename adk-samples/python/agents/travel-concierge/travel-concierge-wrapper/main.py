from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
from agent_client import send_to_adk

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Chat server running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = await send_to_adk(req.text)
    return ChatResponse(response=reply)
