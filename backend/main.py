from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uuid
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Any, Dict, List
import pandas as pd
from typing import List, Optional, Dict, Any

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


APP_NAME = "travel_concierge"
USER_ID = "demo_user"

class MessageRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "API is working!"}

@app.post("/chat")
async def chat_with_agent(req: MessageRequest):
    print("Received:", req.message)
    
    try:
        session_id = str(uuid.uuid4())[:8]
        base_url = "http://localhost:8000"
        session_url = f"{base_url}/apps/{APP_NAME}/users/{USER_ID}/sessions/{session_id}"
        run_url = f"{base_url}/run"

        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            try:
                # Try to create session
                await client.post(session_url)
                
                # Try to run the AI service
                res = await client.post(run_url, json={
                    "appName": APP_NAME,
                    "userId": USER_ID,
                    "sessionId": session_id,
                    "newMessage": {
                        "parts": [{"text": req.message}],
                        "role": "USER"
                    },
                    "streaming": False
                })
                
                res.raise_for_status()
                data = res.json()
                
            except httpx.ConnectError:
                # AI service is not available, return mock response
                print("⚠️ AI service not available, returning mock response")
                return get_mock_response(req.message)
            except httpx.HTTPStatusError as e:
                print(f"⚠️ AI service returned error: {e}")
                return get_mock_response(req.message)
            except Exception as e:
                print(f"⚠️ Unexpected error with AI service: {e}")
                return get_mock_response(req.message)

        # Process the response if AI service worked
        parsed_data: List[Dict[str, Any]] = data
        places_data = []
        text_replies = []

        for entry in parsed_data:
            # Extract places
            actions = entry.get("actions", {})
            state_delta = actions.get("stateDelta", {})
            poi = state_delta.get("poi", {})

            if isinstance(poi, dict):
                places = poi.get("places", [])
                if isinstance(places, list):
                    places_data.extend(places)

            # Extract text responses
            content = entry.get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                if "text" in part and isinstance(part["text"], str):
                    text_replies.append(part["text"])

        # ✅ Output result preview
        print("✅ Places:")
        for place in places_data:
            print("-", place.get("place_name"))

        print("\n✅ Text Replies:")
        for text in text_replies:
            print("-", text[:100], "...\n")

        return {"reply": places_data, "text": text_replies}
        
    except Exception as e:
        print(f"❌ Error in chat_with_agent: {e}")
        return get_mock_response(req.message)

def get_mock_response(message: str) -> Dict[str, Any]:
    """Return a mock response when AI service is unavailable"""
    message_lower = message.lower()
    
    # Mock places data based on common travel queries
    mock_places = []
    mock_text = []
    
    if any(word in message_lower for word in ["india", "indian", "taj", "delhi", "mumbai"]):
        mock_places = [
            {
                "place_name": "Taj Mahal",
                "address": "Agra, Uttar Pradesh, India",
                "lat": "27.1751",
                "long": "78.0421",
                "review_ratings": "4.8",
                "highlights": "Iconic ivory-white marble mausoleum, a UNESCO World Heritage Site",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/1280px-Taj_Mahal_%28Edited%29.jpeg"
            },
            {
                "place_name": "Gateway of India",
                "address": "Mumbai, Maharashtra, India",
                "lat": "18.9219",
                "long": "72.8347",
                "review_ratings": "4.6",
                "highlights": "Iconic arch monument and popular tourist attraction",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Gateway_of_India_in_Mumbai.jpg/1280px-Gateway_of_India_in_Mumbai.jpg"
            }
        ]
        mock_text = ["India offers incredible experiences! Here are some popular destinations you might enjoy."]
    
    elif any(word in message_lower for word in ["japan", "tokyo", "kyoto", "osaka"]):
        mock_places = [
            {
                "place_name": "Mount Fuji",
                "address": "Fuji-Hakone-Izu National Park, Japan",
                "lat": "35.3606",
                "long": "138.7274",
                "review_ratings": "4.9",
                "highlights": "Japan's highest mountain and iconic symbol",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Chuurei-tou_Fujiyoshida_17025277650_c59733cd6c_o.jpg/1280px-Chuurei-tou_Fujiyoshida_17025277650_c59733cd6c_o.jpg"
            },
            {
                "place_name": "Senso-ji Temple",
                "address": "Asakusa, Tokyo, Japan",
                "lat": "35.7148",
                "long": "139.7967",
                "review_ratings": "4.7",
                "highlights": "Tokyo's oldest temple and popular tourist destination",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Senso-ji_Temple_Tokyo_Japan.jpg/1280px-Senso-ji_Temple_Tokyo_Japan.jpg"
            }
        ]
        mock_text = ["Japan is a fascinating country with rich culture and beautiful landscapes!"]
    
    elif any(word in message_lower for word in ["paris", "france", "eiffel", "louvre"]):
        mock_places = [
            {
                "place_name": "Eiffel Tower",
                "address": "Champ de Mars, Paris, France",
                "lat": "48.8584",
                "long": "2.2945",
                "review_ratings": "4.6",
                "highlights": "Iconic iron lattice tower and symbol of Paris",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/1280px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg"
            },
            {
                "place_name": "Louvre Museum",
                "address": "Rue de Rivoli, Paris, France",
                "lat": "48.8606",
                "long": "2.3376",
                "review_ratings": "4.7",
                "highlights": "World's largest art museum and historic monument",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Louvre_Museum_Wikimedia_Commons.jpg/1280px-Louvre_Museum_Wikimedia_Commons.jpg"
            }
        ]
        mock_text = ["Paris is the city of love and art! Here are some must-visit attractions."]
    
    else:
        # Generic response for other queries
        mock_places = [
            {
                "place_name": "Sample Destination",
                "address": "Sample Address",
                "lat": "0.0",
                "long": "0.0",
                "review_ratings": "4.5",
                "highlights": "A wonderful place to visit",
                "image_url": "https://via.placeholder.com/400x300?text=Travel+Destination"
            }
        ]
        mock_text = [f"I'd be happy to help you plan your trip to {message}! Here are some suggestions to get you started."]
    
    return {"reply": mock_places, "text": mock_text}



"""

json being sent to the `/plan-trip` endpoint:

{
  "destination": "Paris",
  "travel_dates": {
    "start": "2025-08-01",
    "end": "2025-08-07"
  },
  "interests": ["art", "food", "sightseeing"]
}
"""
class TripRequest(BaseModel):
    destination: Optional[str] = None
    travel_dates: Optional[Dict[str, str]] = None  # {"start": "2025-08-01", "end": "2025-08-07"}
    interests: Optional[List[str]] = None

@app.post("/plan-trip")
async def plan_trip(req: TripRequest):
    BASE_URL = "http://localhost:8000"
    missing_info = []

    if not req.destination:
        missing_info.append("destination")
    if not req.travel_dates or "start" not in req.travel_dates or "end" not in req.travel_dates:
        missing_info.append("travel_dates")
    if not req.interests:
        missing_info.append("interests")

    if missing_info:
        return {
            "status": "incomplete",
            "missing_info": missing_info,
            "prompt": f"Please provide the following missing info: {', '.join(missing_info)}"
        }

    session_id = str(uuid.uuid4())[:8]
    session_url = f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{session_id}"
    run_url = f"{BASE_URL}/run"

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        try:
            await client.post(session_url)
            response = await client.post(run_url, json={
                "appName": APP_NAME,
                "userId": USER_ID,
                "sessionId": session_id,
                "newMessage": {
                    "parts": [{
                        "text": f"Plan a trip to {req.destination} from {req.travel_dates['start']} to {req.travel_dates['end']} with a focus on {', '.join(req.interests)}."
                    }],
                    "role": "USER"
                },
                "streaming": False
            })
            response.raise_for_status()
            data = response.json()
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process trip planning: {e}")

    return {
        "status": "success",
        "itinerary": data
    } 

""""

🟡 1. If required fields are missing:

{
  "status": "incomplete",
  "missing_info": ["destination", "travel_dates"],
  "prompt": "Please provide the following missing info: destination, travel_dates"
}



🟢 2. If all required data is present and the backend call succeeds:

{
  "status": "success",
  "itinerary": { 
    // whatever the ADK `/run` endpoint returns as JSON
  }
}



🔴 3. If there’s an internal error during the HTTP call:

{
  "detail": "Failed to process trip planning: <error message>"
}


"""
#uvicorn backend.main:app --reload --port 8001
