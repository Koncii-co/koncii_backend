"""
Main entry point for the Travel Concierge API
This file is used by Gunicorn to start the FastAPI application
"""

from travel_concierge.api import app

# Export the app for Gunicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000) 