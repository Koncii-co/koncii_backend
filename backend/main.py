from fastapi import FastAPI, Request
from pydantic import BaseModel
import uuid
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Any, Dict, List
import pandas as pd

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
    session_id = str(uuid.uuid4())[:8]
    base_url = "http://localhost:8000"
    session_url = f"{base_url}/apps/{APP_NAME}/users/{USER_ID}/sessions/{session_id}"
    run_url = f"{base_url}/run"

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        await client.post(session_url)
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
    # data=[{'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'root_agent', 'actions': {'stateDelta': {'_time': '2025-06-21 03:43:04.607723', '_itin_initialized': True, 'user_profile': {'passport_nationality': 'US Citizen', 'seat_preference': 'window', 'food_preference': 'vegan', 'allergies': [], 'likes': [], 'dislikes': [], 'price_sensitivity': [], 'home': {'event_type': 'home', 'address': '6420 Sequence Dr #400, San Diego, CA 92121, United States', 'local_prefer_mode': 'drive'}}, 'itinerary': {}, 'origin': '', 'destination': '', 'start_date': '', 'end_date': '', 'outbound_flight_selection': '', 'outbound_seat_number': '', 'return_flight_selection': '', 'return_seat_number': '', 'hotel_selection': '', 'room_selection': '', 'poi': '', 'itinerary_datetime': '', 'itinerary_start_date': '', 'itinerary_end_date': ''}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'id': 'LOq19VSf', 'timestamp': 1750491784.607755}, {'content': {'parts': [{'functionCall': {'id': 'adk-671e9485-5693-4289-9602-4c7bb421dc0b', 'args': {'agent_name': 'inspiration_agent'}, 'name': 'transfer_to_agent'}}], 'role': 'model'}, 'usageMetadata': {'candidatesTokenCount': 21, 'promptTokenCount': 963, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 963}], 'thoughtsTokenCount': 94, 'totalTokenCount': 1078}, 'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'root_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'longRunningToolIds': [], 'id': '5IPKIDxl', 'timestamp': 1750491784.608411}, {'content': {'parts': [{'functionResponse': {'id': 'adk-671e9485-5693-4289-9602-4c7bb421dc0b', 'name': 'transfer_to_agent', 'response': {'result': None}}}], 'role': 'user'}, 'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'root_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'transferToAgent': 'inspiration_agent', 'requestedAuthConfigs': {}}, 'id': 'qYTKamci', 'timestamp': 1750491785.860861}, {'content': {'parts': [{'functionCall': {'id': 'adk-f8dec78e-5692-4c1e-a740-02c1db9c175e', 'args': {'request': 'India'}, 'name': 'poi_agent'}}], 'role': 'model'}, 'usageMetadata': {'candidatesTokenCount': 15, 'promptTokenCount': 1318, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 1318}], 'thoughtsTokenCount': 102, 'totalTokenCount': 1435}, 'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'inspiration_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'longRunningToolIds': [], 'id': 'bECLDun8', 'timestamp': 1750491785.862088}, {'content': {'parts': [{'functionResponse': {'id': 'adk-f8dec78e-5692-4c1e-a740-02c1db9c175e', 'name': 'poi_agent', 'response': {'places': [{'place_name': 'Taj Mahal', 'address': 'Dharmapuri, Forest Colony, Tajganj, Agra, Uttar Pradesh 282001, India', 'lat': '27.1751', 'long': '78.0421', 'review_ratings': '4.8', 'highlights': 'Iconic ivory-white marble mausoleum, a UNESCO World Heritage Site, and one of the New7Wonders of the World.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/1280px-Taj_Mahal_%28Edited%29.jpeg', 'map_url': '', 'place_id': ''}, {'place_name': 'Gateway of India', 'address': 'Apollo Bunder, Colaba, Mumbai, Maharashtra 400001, India', 'lat': '18.9219', 'long': '72.8347', 'review_ratings': '4.6', 'highlights': 'An iconic arch monument built to commemorate the landing of King George V and Queen Mary at Apollo Bunder in 1911.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Gateway_of_India_in_Mumbai.jpg/1280px-Gateway_of_India_in_Mumbai.jpg', 'map_url': '', 'place_id': ''}, {'place_name': 'Amber Fort', 'address': 'Devisinghpura, Amer, Jaipur, Rajasthan 302028, India', 'lat': '26.9859', 'long': '75.8513', 'review_ratings': '4.7', 'highlights': 'A magnificent fort located in Amer, a town near Jaipur, known for its artistic Hindu style elements and grand palaces.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Amber_Fort_Jaipur_Rajasthan.jpg/1280px-Amber_Fort_Jaipur_Rajasthan.jpg', 'map_url': '', 'place_id': ''}, {'place_name': 'Qutub Minar', 'address': 'Mehrauli, New Delhi, Delhi 110030, India', 'lat': '28.5244', 'long': '77.1855', 'review_ratings': '4.6', 'highlights': 'A UNESCO World Heritage Site, this is a 73-meter tall tapering tower of five storeys, built in 1193 by Qutab-ud-din Aibak.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Qutub_Minar_Delhi.JPG/1280px-Qutub_Minar_Delhi.JPG', 'map_url': '', 'place_id': ''}, {'place_name': 'Varanasi Ghats', 'address': 'Varanasi, Uttar Pradesh, India', 'lat': '25.3087', 'long': '83.0076', 'review_ratings': '4.7', 'highlights': 'The steps leading to the banks of the River Ganges, significant for religious rituals, bathing, and cremation ceremonies.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Ghats_of_Varanasi_on_the_River_Ganges.jpg/1280px-Ghats_of_Varanasi_on_the_River_Ganges.jpg', 'map_url': '', 'place_id': ''}]}}}], 'role': 'user'}, 'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'inspiration_agent', 'actions': {'stateDelta': {'poi': {'places': [{'place_name': 'Taj Mahal', 'address': 'Dharmapuri, Forest Colony, Tajganj, Agra, Uttar Pradesh 282001, India', 'lat': '27.1751', 'long': '78.0421', 'review_ratings': '4.8', 'highlights': 'Iconic ivory-white marble mausoleum, a UNESCO World Heritage Site, and one of the New7Wonders of the World.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/1280px-Taj_Mahal_%28Edited%29.jpeg', 'map_url': None, 'place_id': None}, {'place_name': 'Gateway of India', 'address': 'Apollo Bunder, Colaba, Mumbai, Maharashtra 400001, India', 'lat': '18.9219', 'long': '72.8347', 'review_ratings': '4.6', 'highlights': 'An iconic arch monument built to commemorate the landing of King George V and Queen Mary at Apollo Bunder in 1911.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Gateway_of_India_in_Mumbai.jpg/1280px-Gateway_of_India_in_Mumbai.jpg', 'map_url': None, 'place_id': None}, {'place_name': 'Amber Fort', 'address': 'Devisinghpura, Amer, Jaipur, Rajasthan 302028, India', 'lat': '26.9859', 'long': '75.8513', 'review_ratings': '4.7', 'highlights': 'A magnificent fort located in Amer, a town near Jaipur, known for its artistic Hindu style elements and grand palaces.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Amber_Fort_Jaipur_Rajasthan.jpg/1280px-Amber_Fort_Jaipur_Rajasthan.jpg', 'map_url': None, 'place_id': None}, {'place_name': 'Qutub Minar', 'address': 'Mehrauli, New Delhi, Delhi 110030, India', 'lat': '28.5244', 'long': '77.1855', 'review_ratings': '4.6', 'highlights': 'A UNESCO World Heritage Site, this is a 73-meter tall tapering tower of five storeys, built in 1193 by Qutab-ud-din Aibak.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Qutub_Minar_Delhi.JPG/1280px-Qutub_Minar_Delhi.JPG', 'map_url': None, 'place_id': None}, {'place_name': 'Varanasi Ghats', 'address': 'Varanasi, Uttar Pradesh, India', 'lat': '25.3087', 'long': '83.0076', 'review_ratings': '4.7', 'highlights': 'The steps leading to the banks of the River Ganges, significant for religious rituals, bathing, and cremation ceremonies.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Ghats_of_Varanasi_on_the_River_Ganges.jpg/1280px-Ghats_of_Varanasi_on_the_River_Ganges.jpg', 'map_url': None, 'place_id': None}]}}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'id': 'thAkq5vZ', 'timestamp': 1750491792.415954}, {'content': {'parts': [{'functionCall': {'id': 'adk-67d7af4c-7dbe-4990-8cf3-0fbbc71e845a', 'args': {'key': 'poi'}, 'name': 'map_tool'}}], 'role': 'model'}, 'usageMetadata': {'candidatesTokenCount': 15, 'promptTokenCount': 2194, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 2194}], 'thoughtsTokenCount': 72, 'totalTokenCount': 2281}, 'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'inspiration_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'longRunningToolIds': [], 'id': 'H5uMV9QV', 'timestamp': 1750491792.417474}, {'content': {'parts': [{'functionResponse': {'id': 'adk-67d7af4c-7dbe-4990-8cf3-0fbbc71e845a', 'name': 'map_tool', 'response': {'places': [{'place_name': 'Taj Mahal', 'address': 'Dharmapuri, Forest Colony, Tajganj, Agra, Uttar Pradesh 282001, India', 'lat': '27.1751', 'long': '78.0421', 'review_ratings': '4.8', 'highlights': 'Iconic ivory-white marble mausoleum, a UNESCO World Heritage Site, and one of the New7Wonders of the World.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/1280px-Taj_Mahal_%28Edited%29.jpeg', 'map_url': None, 'place_id': None}, {'place_name': 'Gateway of India', 'address': 'Apollo Bunder, Colaba, Mumbai, Maharashtra 400001, India', 'lat': '18.9219', 'long': '72.8347', 'review_ratings': '4.6', 'highlights': 'An iconic arch monument built to commemorate the landing of King George V and Queen Mary at Apollo Bunder in 1911.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Gateway_of_India_in_Mumbai.jpg/1280px-Gateway_of_India_in_Mumbai.jpg', 'map_url': None, 'place_id': None}, {'place_name': 'Amber Fort', 'address': 'Devisinghpura, Amer, Jaipur, Rajasthan 302028, India', 'lat': '26.9859', 'long': '75.8513', 'review_ratings': '4.7', 'highlights': 'A magnificent fort located in Amer, a town near Jaipur, known for its artistic Hindu style elements and grand palaces.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Amber_Fort_Jaipur_Rajasthan.jpg/1280px-Amber_Fort_Jaipur_Rajasthan.jpg', 'map_url': None, 'place_id': None}, {'place_name': 'Qutub Minar', 'address': 'Mehrauli, New Delhi, Delhi 110030, India', 'lat': '28.5244', 'long': '77.1855', 'review_ratings': '4.6', 'highlights': 'A UNESCO World Heritage Site, this is a 73-meter tall tapering tower of five storeys, built in 1193 by Qutab-ud-din Aibak.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Qutub_Minar_Delhi.JPG/1280px-Qutub_Minar_Delhi.JPG', 'map_url': None, 'place_id': None}, {'place_name': 'Varanasi Ghats', 'address': 'Varanasi, Uttar Pradesh, India', 'lat': '25.3087', 'long': '83.0076', 'review_ratings': '4.7', 'highlights': 'The steps leading to the banks of the River Ganges, significant for religious rituals, bathing, and cremation ceremonies.', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Ghats_of_Varanasi_on_the_River_Ganges.jpg/1280px-Ghats_of_Varanasi_on_the_River_Ganges.jpg', 'map_url': None, 'place_id': None}]}}}], 'role': 'user'}, 'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'inspiration_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'id': 'zcTZwHle', 'timestamp': 1750491794.269105}, {'content': {'parts': [{'text': 'India offers a wealth of incredible experiences! Here are a few popular places and activities to consider:\n\n*   **Taj Mahal** in Agra: An iconic ivory-white marble mausoleum, a UNESCO World Heritage Site, and one of the New7Wonders of the World.\n*   **Gateway of India** in Mumbai: An iconic arch monument built to commemorate the landing of King George V and Queen Mary in 1911.\n*   **Amber Fort** in Jaipur: A magnificent fort known for its artistic Hindu style elements and grand palaces.\n*   **Qutub Minar** in New Delhi: A UNESCO World Heritage Site, this is a 73-meter tall tapering tower of five storeys, built in 1193.\n*   **Varanasi Ghats** in Varanasi: The steps leading to the banks of the River Ganges, significant for religious rituals, bathing, and cremation ceremonies.\n\nDo any of these pique your interest, or would you like to explore other types of activities or regions in India?'}], 'role': 'model'}, 'usageMetadata': {'candidatesTokenCount': 217, 'promptTokenCount': 3080, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 3080}], 'thoughtsTokenCount': 199, 'totalTokenCount': 3496}, 'invocationId': 'e-cd9b9d38-9076-45b7-ae14-905747bfbcf6', 'author': 'inspiration_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'id': 'GV7olBdK', 'timestamp': 1750491794.271551}]  

    parsed_data: List[Dict[str, Any]] = data  # your provided list
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

    return {"reply":places_data,"text":text_replies}

    


#uvicorn backend.main:app --reload --port 8001
