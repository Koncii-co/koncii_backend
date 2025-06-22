# Travel Concierge API Server

This document explains how to run the Travel Concierge agent as a FastAPI server using uvicorn.

## Prerequisites

1. **Python 3.11+** installed
2. **Virtual environment** activated (`.venv`)
3. **Google Cloud Project** with Vertex AI enabled
4. **Google Maps Platform Places API** key
5. **Environment variables** configured

## Setup

### 1. Activate Virtual Environment

```bash
source backend/.venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Google Maps Platform Places API
GOOGLE_PLACES_API_KEY=your-places-api-key

# Optional: Storage bucket for deployment
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```

### 4. Authenticate with Google Cloud

```bash
gcloud auth application-default login
```

## Running the Server

### Option 1: Using the Run Script (Recommended)

```bash
cd backend
python run_server.py
```

### Option 2: Using Uvicorn Directly

```bash
cd backend
uvicorn travel_concierge.api:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Chat Endpoint

- `POST /chat` - Send a message to the AI travel concierge

**Request:**
```json
{
  "message": "I need help planning a trip to Paris"
}
```

**Response:**
```json
{
  "response": "I can help you plan a trip to Paris! To start, I need a few more details...",
  "status": "success"
}
```

### Health Check

- `GET /health` - Check if the server is running

**Response:**
```json
{
  "status": "healthy",
  "service": "travel_concierge_api"
}
```

## Example Usage

### Send a Message

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need help planning a trip to Paris"
  }'
```

### Get Health Status

```bash
curl -X GET "http://localhost:8000/health"
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Frontend Integration

The API is designed to work seamlessly with the Koncii frontend. The frontend can simply send messages to the `/chat` endpoint without any session management.

### Frontend Example

```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Plan a 7-day trip to Japan'
  })
});

const data = await response.json();
console.log(data.response); // AI response
```

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Ensure all required environment variables are set in your `.env` file
   - Check that your Google Cloud project has Vertex AI enabled

2. **Authentication Errors**
   - Run `gcloud auth application-default login` to authenticate
   - Ensure your Google Cloud project has the necessary APIs enabled

3. **Import Errors**
   - Make sure you're in the correct directory (`backend/`)
   - Ensure the virtual environment is activated
   - Check that all dependencies are installed

4. **Port Already in Use**
   - Change the port in the uvicorn command: `--port 8001`
   - Or kill the process using the port: `lsof -ti:8000 | xargs kill -9`

### Debug Mode

To run with debug logging:

```bash
uvicorn travel_concierge.api:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## Development

The server includes:
- **CORS middleware** for frontend integration
- **Simplified API** - no session management required
- **Error handling** with proper HTTP status codes
- **API documentation** via FastAPI's automatic docs

## Production Deployment

For production deployment:
1. Remove `--reload` flag
2. Configure proper CORS origins
3. Use a production ASGI server like Gunicorn
4. Set up proper environment variables
5. Configure domain mapping for your production domain

## Architecture

The simplified API architecture:
- **Single endpoint** (`/chat`) for all interactions
- **Stateless design** - each request is independent
- **Automatic session creation** - handled internally by the ADK
- **Clean response format** - just `response` and `status` 