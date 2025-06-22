"""
FastAPI application for Travel Concierge Agent
"""

import os
import asyncio
import uuid
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from travel_concierge.agent import root_agent

# Load environment variables
load_dotenv()

# Set up Google Cloud authentication for production
def setup_google_auth():
    """Set up Google Cloud authentication for production deployment"""
    # Check if we have service account JSON in environment
    credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if credentials_json:
        try:
            # Parse the JSON and write to a temporary file
            credentials_data = json.loads(credentials_json)
            credentials_path = '/tmp/google-credentials.json'
            with open(credentials_path, 'w') as f:
                json.dump(credentials_data, f)
            
            # Set the environment variable to point to the file
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            print("✅ Google Cloud authentication configured from environment")
        except Exception as e:
            print(f"⚠️ Warning: Failed to set up Google Cloud credentials: {e}")
    else:
        print("ℹ️ Using default Google Cloud authentication")

# Initialize Google Cloud authentication
setup_google_auth()

# Create FastAPI app
app = FastAPI(
    title="Travel Concierge API",
    description="AI-powered travel concierge service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize session service
session_service = InMemorySessionService()

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the travel concierge agent"""
    try:
        # Generate unique session and user IDs for each request
        session_id = str(uuid.uuid4())
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # Create session in session service
        await session_service.create_session(
            app_name="travel-concierge",
            user_id=user_id,
            session_id=session_id
        )
        
        # Create content from message
        content = Content(
            parts=[Part.from_text(text=request.message)],
            role="user"
        )
        
        # Create runner for this request
        runner = Runner(
            app_name="travel-concierge",
            agent=root_agent,
            session_service=session_service
        )
        
        # Run the agent and collect response
        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            # Extract text from events
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
                elif hasattr(event.content, 'text'):
                    response_text += event.content.text
        
        # If no response text was collected, provide a default response
        if not response_text.strip():
            response_text = "I'm processing your request. Please try again."
        
        return ChatResponse(
            response=response_text,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "travel_concierge_api",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Travel Concierge API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "chat": "/chat"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 