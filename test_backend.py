#!/usr/bin/env python3
"""
Simple test script to verify the backend works
"""

import asyncio
import httpx
import json

async def test_backend():
    """Test the backend endpoints"""
    
    # Test health check
    print("🔍 Testing health check...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8001/")
            print(f"✅ Health check: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
    
    # Test chat endpoint
    print("\n🔍 Testing chat endpoint...")
    test_messages = [
        "I want to visit India",
        "Tell me about Japan",
        "What's in Paris?",
        "Random travel query"
    ]
    
    async with httpx.AsyncClient() as client:
        for message in test_messages:
            try:
                response = await client.post(
                    "http://localhost:8001/chat",
                    json={"message": message},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    places = data.get("reply", [])
                    texts = data.get("text", [])
                    
                    print(f"✅ Chat '{message}': {len(places)} places, {len(texts)} texts")
                    if places:
                        print(f"   📍 First place: {places[0].get('place_name', 'N/A')}")
                    if texts:
                        print(f"   💬 First text: {texts[0][:50]}...")
                else:
                    print(f"❌ Chat '{message}': {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Chat '{message}' failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing Koncii Backend...")
    print("Make sure the backend is running on http://localhost:8001")
    print("=" * 50)
    
    asyncio.run(test_backend())
    
    print("\n" + "=" * 50)
    print("✅ Backend test completed!") 