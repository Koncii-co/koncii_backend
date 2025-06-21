import httpx
import uuid

APP_NAME = "travel_concierge"
USER_ID = "demo_user"
SESSION_ID = str(uuid.uuid4())[:8]  # Generate a short session ID

async def send_to_adk(text: str) -> str:
    base_url = "http://localhost:8000"
    session_url = f"{base_url}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
    run_url = f"{base_url}/run"

    async with httpx.AsyncClient() as client:
        # Step 1: Create session
        await client.post(session_url)

        # Step 2: Send message to /run
        res = await client.post(run_url, json={
            "appName": APP_NAME,
            "userId": USER_ID,
            "sessionId": SESSION_ID,
            "newMessage": {
                "parts": [
                    {
                        "text": text
                    }
                ],
                "role": "USER"
            },
            "streaming": False
        })

        # Step 3: Parse response safely
        res.raise_for_status()
        data = res.json()
        if isinstance(data, list) and data:
            parts = data[0].get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]
        return "No valid response from agent."


if __name__ == "__main__":
    import asyncio

    async def main():
        reply = await send_to_adk("What’s the best city to visit in July?")
        print("Reply from agent:", reply)

    asyncio.run(main())
#(.venv) (base) manveersohal@Manveers-MacBook-Pro travel-concierge-wrapper % uvicorn backend.main:app --reload --port 9000 to run the agentic backend