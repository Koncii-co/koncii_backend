#!/usr/bin/env python3
"""
Test script for the /mcp-airbnb endpoint
"""

import requests
import json
import time

def test_mcp_airbnb_endpoint():
    """Test the /mcp-airbnb endpoint with an Airbnb search request"""
    
    # API endpoint
    url = "http://localhost:8000/mcp-airbnb"
    
    # Test message that should trigger Airbnb search
    test_message = "Find me an airbnb in San Diego, April 9th, to april 13th, no flights nor itinerary needed. No need to confirm, simply return 5 choices, remember to include urls."
    
    print("🧪 Testing /mcp-airbnb endpoint")
    print(f"📤 Sending request to: {url}")
    print(f"💬 Message: {test_message}")
    print("-" * 80)
    
    try:
        # Send POST request
        response = requests.post(
            url,
            json={"message": test_message},
            headers={"Content-Type": "application/json"},
            timeout=120  # 2 minute timeout for MCP operations
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! Response received:")
            print(f"📝 Status: {data.get('status')}")
            print(f"💬 Response: {data.get('response')}")
            
            # Show function calls if any
            if data.get('function_calls'):
                print(f"🔧 Function Calls: {json.dumps(data['function_calls'], indent=2)}")
            
            # Show function responses if any
            if data.get('function_responses'):
                print(f"📋 Function Responses: {json.dumps(data['function_responses'], indent=2)}")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response Text: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout: Request took too long (MCP server might be starting up)")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection Error: Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

def test_health_endpoint():
    """Test the health endpoint to ensure server is running"""
    
    url = "http://localhost:8000/health"
    
    print("\n🏥 Testing health endpoint...")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is healthy: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting MCP Airbnb Endpoint Test")
    print("=" * 80)
    
    # First check if server is running
    if test_health_endpoint():
        # Wait a moment for server to be ready
        print("\n⏳ Waiting 3 seconds for server to be ready...")
        time.sleep(3)
        
        # Test the MCP Airbnb endpoint
        test_mcp_airbnb_endpoint()
    else:
        print("\n❌ Server is not running. Please start the server first:")
        print("   python main.py")
        print("   or")
        print("   uvicorn travel_concierge.api:app --host 0.0.0.0 --port 8000")
    
    print("\n" + "=" * 80)
    print("�� Test completed") 