#!/usr/bin/env python3
"""
Script to run the Travel Concierge FastAPI server
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def main():
    """Run the FastAPI server"""
    
    # Check if required environment variables are set
    required_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION", 
        "GOOGLE_PLACES_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        print("See the README for setup instructions.")
        sys.exit(1)
    
    print("🚀 Starting Travel Concierge API Server...")
    print(f"📍 Project: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
    print(f"🌍 Location: {os.getenv('GOOGLE_CLOUD_LOCATION')}")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Run the server
    uvicorn.run(
        "travel_concierge.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 