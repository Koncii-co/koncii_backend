#!/usr/bin/env python3
"""
Test script to verify the new debugging features
"""

import requests
import json
import time

def test_debug_endpoint():
    """Test the new debug endpoint"""
    print("🔍 Testing debug endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/debug", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Debug endpoint working")
            print("📊 Debug info:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Debug endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Debug endpoint error: {e}")
        return False

def test_mcp_endpoint():
    """Test the MCP endpoint with fallback handling"""
    print("🔍 Testing MCP endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:8000/mcp-airbnb",
            json={"message": "Find me a place to stay in Seattle"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ MCP endpoint working")
            print(f"📊 Status: {data.get('status', 'unknown')}")
            print(f"📊 Response: {data.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ MCP endpoint failed with status {response.status_code}")
            print(f"📊 Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ MCP endpoint error: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working")
            print(f"📊 Status: {data}")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print("Make sure the server is running on http://localhost:8000")
    print()
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    tests = [
        test_health_endpoint,
        test_debug_endpoint,
        test_mcp_endpoint
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 