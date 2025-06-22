#!/bin/bash

# Start script for Render deployment

echo "🚀 Starting Travel Concierge API on Render..."

# Check if required environment variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "❌ Error: GOOGLE_CLOUD_PROJECT environment variable is not set"
    exit 1
fi

if [ -z "$GOOGLE_PLACES_API_KEY" ]; then
    echo "❌ Error: GOOGLE_PLACES_API_KEY environment variable is not set"
    exit 1
fi

echo "✅ Environment variables validated"
echo "📍 Project: $GOOGLE_CLOUD_PROJECT"
echo "🌍 Location: ${GOOGLE_CLOUD_LOCATION:-us-central1}"
echo "🔑 Places API: Configured"
echo "📖 API Documentation: https://$RENDER_EXTERNAL_HOSTNAME/docs"
echo "🔍 Health Check: https://$RENDER_EXTERNAL_HOSTNAME/health"

# Start the application with Gunicorn
exec gunicorn travel_concierge.api:app -c gunicorn.conf.py 