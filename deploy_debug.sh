#!/bin/bash

# Comprehensive Deployment and Debugging Script for Render
# This script helps deploy and debug the Travel Concierge API on Render

set -e

echo "🚀 Starting comprehensive deployment and debugging process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    print_error "Please run this script from the backend directory"
    exit 1
fi

print_status "Current directory: $(pwd)"

# Step 1: Environment Setup Check
print_status "Step 1: Checking environment setup..."

# Check if .env file exists
if [ -f ".env" ]; then
    print_success ".env file found"
    # Check for required environment variables
    if grep -q "GOOGLE_AI_API_KEY" .env; then
        print_success "GOOGLE_AI_API_KEY found in .env"
    else
        print_warning "GOOGLE_AI_API_KEY not found in .env"
    fi
    
    if grep -q "GOOGLE_APPLICATION_CREDENTIALS_JSON" .env; then
        print_success "GOOGLE_APPLICATION_CREDENTIALS_JSON found in .env"
    else
        print_warning "GOOGLE_APPLICATION_CREDENTIALS_JSON not found in .env"
    fi
else
    print_warning ".env file not found"
fi

# Step 2: Python Environment Check
print_status "Step 2: Checking Python environment..."

# Check Python version
python_version=$(python3 --version 2>&1)
print_status "Python version: $python_version"

# Check if required packages are installed
print_status "Checking required packages..."
python3 -c "import fastapi, google.adk, dotenv" 2>/dev/null && print_success "Core packages available" || print_error "Missing core packages"

# Step 3: Node.js Environment Check
print_status "Step 3: Checking Node.js environment..."

# Check Node.js
if command -v node &> /dev/null; then
    node_version=$(node --version)
    print_success "Node.js version: $node_version"
else
    print_error "Node.js not found"
fi

# Check npm
if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    print_success "npm version: $npm_version"
else
    print_error "npm not found"
fi

# Check npx
if command -v npx &> /dev/null; then
    npx_version=$(npx --version)
    print_success "npx version: $npx_version"
else
    print_error "npx not found"
fi

# # Step 4: MCP Server Check
# print_status "Step 4: Checking MCP server availability..."

# # Test MCP server
# if command -v npx &> /dev/null; then
#     print_status "Testing MCP server availability..."
#     if npx -y @openbnb/mcp-server-airbnb --help &>/dev/null; then
#         print_success "MCP server is available"
#     else
#         print_warning "MCP server test failed"
#         print_status "Attempting to install MCP server globally..."
#         npm install -g @openbnb/mcp-server-airbnb 2>/dev/null && print_success "MCP server installed globally" || print_error "Failed to install MCP server"
#     fi
# else
#     print_error "Cannot test MCP server - npx not available"
# fi

# Step 5: Local API Test
print_status "Step 5: Testing local API..."

# Start the server in background
print_status "Starting local server for testing..."
python3 main.py &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test health endpoint
if curl -s http://localhost:8000/health > /dev/null; then
    print_success "Health endpoint working"
else
    print_error "Health endpoint failed"
fi

# Test debug endpoint
if curl -s http://localhost:8000/debug > /dev/null; then
    print_success "Debug endpoint working"
    print_status "Debug info:"
    curl -s http://localhost:8000/debug | python3 -m json.tool
else
    print_error "Debug endpoint failed"
fi

# Test chat endpoint
print_status "Testing chat endpoint..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello"}' 2>/dev/null || echo "{}")

if echo "$CHAT_RESPONSE" | grep -q "response"; then
    print_success "Chat endpoint working"
else
    print_error "Chat endpoint failed"
    echo "Response: $CHAT_RESPONSE"
fi

# Test MCP endpoint
print_status "Testing MCP endpoint..."
MCP_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp-airbnb \
    -H "Content-Type: application/json" \
    -d '{"message": "Find me a place to stay in Seattle"}' 2>/dev/null || echo "{}")

if echo "$MCP_RESPONSE" | grep -q "response"; then
    print_success "MCP endpoint working"
else
    print_warning "MCP endpoint failed or returned error"
    echo "Response: $MCP_RESPONSE"
fi

# Stop the server
kill $SERVER_PID 2>/dev/null || true

# Step 6: Docker Build Test
print_status "Step 6: Testing Docker build..."

if command -v docker &> /dev/null; then
    print_status "Building Docker image..."
    if docker build -t travel-concierge-test . > docker_build.log 2>&1; then
        print_success "Docker build successful"
        
        # Test Docker container
        print_status "Testing Docker container..."
        docker run -d --name travel-concierge-test -p 8001:8000 travel-concierge-test &
        sleep 10
        
        if curl -s http://localhost:8001/health > /dev/null; then
            print_success "Docker container working"
        else
            print_error "Docker container failed"
        fi
        
        # Cleanup
        docker stop travel-concierge-test 2>/dev/null || true
        docker rm travel-concierge-test 2>/dev/null || true
    else
        print_error "Docker build failed"
        print_status "Docker build log:"
        tail -20 docker_build.log
    fi
else
    print_warning "Docker not available - skipping Docker test"
fi

# Step 7: Render Deployment Check
print_status "Step 7: Render deployment preparation..."

# Check render.yaml
if [ -f "render.yaml" ]; then
    print_success "render.yaml found"
    print_status "Render configuration:"
    cat render.yaml
else
    print_error "render.yaml not found"
fi

# Check Dockerfile
if [ -f "Dockerfile" ]; then
    print_success "Dockerfile found"
    print_status "Dockerfile contents:"
    cat Dockerfile
else
    print_error "Dockerfile not found"
fi

# Step 8: Environment Variables for Render
print_status "Step 8: Environment variables for Render deployment..."

cat << EOF

📋 REQUIRED ENVIRONMENT VARIABLES FOR RENDER:

1. GOOGLE_AI_API_KEY=your_google_ai_api_key_here
2. GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}
3. ENVIRONMENT=production

🔧 SETTING UP ENVIRONMENT VARIABLES ON RENDER:

1. Go to your Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add the following variables:

   Key: GOOGLE_AI_API_KEY
   Value: [Your Google AI API Key]

   Key: GOOGLE_APPLICATION_CREDENTIALS_JSON
   Value: [Your complete service account JSON]

   Key: ENVIRONMENT
   Value: production

5. Save and redeploy

EOF

# Step 9: Troubleshooting Guide
print_status "Step 9: Troubleshooting guide..."

cat << EOF

🔍 TROUBLESHOOTING COMMON ISSUES:

1. MCP Server Issues:
   - Check if Node.js is installed in Docker
   - Verify npx is available
   - Check MCP server installation
   - Look for timeout errors in logs

2. API Key Issues:
   - Verify GOOGLE_AI_API_KEY is set
   - Check for trailing characters in API key
   - Ensure service account JSON is complete

3. Timeout Issues:
   - Check Gunicorn timeout settings
   - Verify MCP server startup time
   - Look for memory constraints

4. Debug Steps:
   - Check /debug endpoint on Render
   - Review Render logs for specific errors
   - Test endpoints individually
   - Verify environment variables

📞 NEXT STEPS:

1. Deploy to Render with the updated configuration
2. Check the /debug endpoint on your Render URL
3. Review Render logs for any errors
4. Test the /mcp-airbnb endpoint
5. If issues persist, check the specific error messages

EOF

print_success "Deployment and debugging script completed!"
print_status "Check the output above for any issues that need to be addressed." 