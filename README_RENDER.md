# Travel Concierge API - Render Deployment Guide

This guide will help you deploy the Travel Concierge API to Render.com.

## 🚀 Quick Deployment

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub/GitLab**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository
   - Select the repository containing this backend

3. **Configure the service**
   - **Name**: `travel-concierge-api`
   - **Root Directory**: `backend` (if your backend is in a subdirectory)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app -c gunicorn.conf.py`

4. **Set Environment Variables**
   - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
   - `GOOGLE_PLACES_API_KEY`: Your Google Places API key
   - `GOOGLE_CLOUD_STORAGE_BUCKET`: Your GCS bucket name (optional)
   - `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Service account JSON (for production)

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Option 2: Manual Configuration

If you prefer to configure manually without render.yaml:

1. **Create a new Web Service** in Render
2. **Connect your repository**
3. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app -c gunicorn.conf.py`
   - **Environment**: Python 3.11

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud project ID | `my-travel-project` |
| `GOOGLE_PLACES_API_KEY` | Google Places API key | `AIza...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLOUD_LOCATION` | Google Cloud region | `us-central1` |
| `GOOGLE_CLOUD_STORAGE_BUCKET` | GCS bucket for file storage | None |
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Service account JSON (production) | None |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI for Gemini | `1` |

## 🏗️ Project Structure

```
backend/
├── main.py                    # Main entry point for Gunicorn
├── travel_concierge/
│   ├── api.py                # FastAPI application
│   ├── agent.py              # Main agent logic
│   └── ...
├── requirements.txt           # Python dependencies
├── gunicorn.conf.py          # Gunicorn configuration
├── render.yaml               # Render deployment config
└── start.sh                  # Start script
```

## 🔍 Health Check

After deployment, you can verify the service is running:

- **Health Check**: `https://your-app-name.onrender.com/health`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **Root**: `https://your-app-name.onrender.com/`

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'main'**
   - Ensure you're in the correct directory (backend/)
   - Check that main.py exists and imports correctly

2. **Import errors for travel_concierge**
   - Verify all dependencies are installed
   - Check that the travel_concierge package is properly structured

3. **Environment variable errors**
   - Ensure all required environment variables are set in Render
   - Check variable names and values

4. **Google Cloud authentication issues**
   - For production, set `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - Ensure the service account has proper permissions

### Debugging Commands

```bash
# Test local import
python -c "from main import app; print('✅ App imported successfully')"

# Test Gunicorn configuration
gunicorn --check-config main:app -c gunicorn.conf.py

# Test local server
python main.py
```

## 🔄 Updating the Deployment

To update your deployment:

1. **Make your changes** to the code
2. **Commit and push** to your repository
3. **Render will automatically** redeploy the service

## 📊 Monitoring

- **Logs**: Available in the Render dashboard
- **Metrics**: CPU, memory, and request metrics
- **Health**: Automatic health checks

## 🔒 Security Considerations

1. **CORS**: Configure `allow_origins` in production
2. **API Keys**: Store sensitive data in environment variables
3. **Authentication**: Implement proper auth for production use
4. **Rate Limiting**: Consider adding rate limiting middleware

## 📞 Support

If you encounter issues:

1. Check the Render logs in the dashboard
2. Verify environment variables are set correctly
3. Test locally with the same configuration
4. Check the troubleshooting section above

---

**Happy Deploying! 🚀** 