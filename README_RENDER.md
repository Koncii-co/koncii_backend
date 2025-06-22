# Deploying Travel Concierge API to Render

This guide will help you deploy your Travel Concierge API to Render, a cloud platform that makes it easy to deploy web services.

## Prerequisites

1. **Google Cloud Project** with Vertex AI enabled
2. **Google Maps Platform Places API** key
3. **Render Account** (free tier available)
4. **Git Repository** with your backend code

## Step 1: Prepare Your Repository

Make sure your backend directory contains all the necessary files:

```
backend/
├── travel_concierge/
│   ├── __init__.py
│   ├── agent.py
│   ├── api.py
│   └── ...
├── requirements.txt
├── gunicorn.conf.py
├── render.yaml
├── Dockerfile
├── .dockerignore
├── start.sh
└── README_RENDER.md
```

## Step 2: Set Up Google Cloud Authentication

### Option A: Service Account (Recommended for Production)

1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. In Render, add the entire JSON content as an environment variable:
   ```
   GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}
   ```

### Option B: Application Default Credentials (Development)

1. Run `gcloud auth application-default login` locally
2. Copy the credentials file to your project
3. Add the file path as an environment variable in Render

## Step 3: Deploy to Render

### Method 1: Using render.yaml (Recommended)

1. **Connect your repository** to Render
2. **Create a new Web Service**
3. **Select your repository** and the `backend` directory
4. **Render will automatically detect** the `render.yaml` configuration
5. **Set environment variables** (see below)
6. **Deploy**

### Method 2: Manual Configuration

If you prefer manual setup:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn travel_concierge.api:app -c gunicorn.conf.py`
- **Environment**: Python 3.11

## Step 4: Configure Environment Variables

In your Render service settings, add these environment variables:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud Project ID | `my-travel-app-123456` |
| `GOOGLE_PLACES_API_KEY` | Google Maps Platform Places API key | `AIzaSyC...` |
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Service account JSON (if using service account) | `{"type": "service_account", ...}` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLOUD_LOCATION` | Google Cloud region | `us-central1` |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI backend | `1` |
| `TRAVEL_CONCIERGE_SCENARIO` | Default scenario file | `travel_concierge/profiles/itinerary_empty_default.json` |

## Step 5: Update Frontend Configuration

Once deployed, update your frontend's API base URL:

```typescript
// In koncii_co_frontend/src/services/aiTravelService.ts
const API_BASE_URL = 'https://your-app-name.onrender.com';
```

## Step 6: Test Your Deployment

### Health Check
```bash
curl https://your-app-name.onrender.com/health
```

### API Test
```bash
curl -X POST "https://your-app-name.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me plan a trip?"}'
```

### API Documentation
Visit: `https://your-app-name.onrender.com/docs`

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is 3.11
   - Verify file paths in your code

2. **Runtime Errors**
   - Check environment variables are set correctly
   - Verify Google Cloud authentication
   - Check logs in Render dashboard

3. **CORS Issues**
   - The API includes CORS middleware for `*` origins
   - For production, consider restricting to your frontend domain

4. **Memory Issues**
   - The starter plan has 512MB RAM
   - Consider upgrading if you experience memory issues

### Logs and Debugging

1. **View Logs**: Go to your Render service dashboard
2. **Real-time Logs**: Use the "Logs" tab for live debugging
3. **Build Logs**: Check the "Events" tab for build issues

### Performance Optimization

1. **Worker Configuration**: Adjust `workers` in `gunicorn.conf.py`
2. **Memory Usage**: Monitor memory usage in Render dashboard
3. **Response Time**: Use the health check endpoint to monitor performance

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to your repository
2. **API Keys**: Use Render's environment variable system
3. **CORS**: Restrict origins in production
4. **HTTPS**: Render provides automatic HTTPS

## Scaling

### Auto-scaling
- Render automatically scales based on traffic
- Starter plan: 0-1 instances
- Pro plan: 0-10 instances

### Manual Scaling
- Upgrade your plan for more resources
- Adjust worker configuration for better performance

## Monitoring

### Health Checks
- Render automatically checks `/health` endpoint
- Failed health checks trigger restarts

### Metrics
- Monitor response times
- Check error rates
- Track memory usage

## Cost Optimization

1. **Starter Plan**: Free tier available
2. **Sleep Mode**: Services sleep after 15 minutes of inactivity
3. **Cold Starts**: First request after sleep may be slower

## Support

- **Render Documentation**: https://render.com/docs
- **Google Cloud Documentation**: https://cloud.google.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

## Example Deployment URL

Once deployed, your API will be available at:
```
https://your-app-name.onrender.com
```

Your frontend can then use this URL to communicate with the AI travel concierge! 