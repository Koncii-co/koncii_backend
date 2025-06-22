#!/bin/bash

# Environment Setup Script for Travel Concierge API

echo "🔧 Setting up environment variables for Travel Concierge API..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating one..."
    cat > .env << EOF
# Local Development Environment
MCP_ENABLED=true
MCP_TIMEOUT=30
NODE_OPTIONS=--max-old-space-size=4096
ENVIRONMENT=development

# Google AI Configuration (for development)
# Add your Google AI API key here
GOOGLE_AI_API_KEY=your-google-ai-api-key-here

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Travel Concierge Configuration
GOOGLE_GENAI_USE_VERTEXAI=0
TRAVEL_CONCIERGE_SCENARIO=travel_concierge/profiles/itinerary_empty_default.json
EOF
    echo "✅ .env file created"
else
    echo "✅ .env file exists"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Edit the .env file and add your Google AI API key:"
echo "   GOOGLE_AI_API_KEY=your-actual-api-key-here"
echo ""
echo "2. You can get a Google AI API key from:"
echo "   https://makersuite.google.com/app/apikey"
echo ""
echo "3. For production, you'll need to set up Google Cloud credentials"
echo "   See env.template for more details"
echo ""
echo "4. After adding your API key, restart the server:"
echo "   python start_server.py" 