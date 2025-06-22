# Travel Concierge API - Debugging and Deployment Guide

This guide covers the comprehensive debugging and robustness improvements made to the Travel Concierge API to help resolve MCP server issues on Render.

## 🚀 What's New

### Enhanced Debugging Features

1. **Environment Debugging at Startup**
   - Automatic environment variable validation
   - Node.js, npm, npx availability checks
   - MCP server availability verification
   - Detailed startup logging

2. **Robust MCP Handling**
   - Graceful fallback when MCP is unavailable
   - Comprehensive error handling and logging
   - Automatic retry mechanisms
   - Status tracking for MCP availability

3. **New Debug Endpoint**
   - `/debug` endpoint for system status
   - Real-time environment checks
   - Node.js and MCP server diagnostics
   - Detailed error reporting

4. **Comprehensive Deployment Script**
   - `deploy_debug.sh` for local testing
   - Environment validation
   - Docker build testing
   - Render deployment preparation

## 📋 Files Modified/Created

### Modified Files
- `travel_concierge/api.py` - Enhanced with debugging and robustness features

### New Files
- `deploy_debug.sh` - Comprehensive deployment and debugging script
- `test_debug.py` - Test script for new debugging features
- `README_DEBUG.md` - This documentation

## 🔧 How to Use

### 1. Local Testing

Start the server:
```bash
python3 main.py
```

Test the new debugging features:
```bash
python3 test_debug.py
```

Run the comprehensive deployment script:
```bash
./deploy_debug.sh
```

### 2. Debug Endpoint

Access the debug endpoint to check system status:
```bash
curl http://localhost:8000/debug
```

This will return detailed information about:
- Environment variables
- Node.js availability
- MCP server status
- System configuration

### 3. MCP Endpoint with Fallback

The `/mcp-airbnb` endpoint now includes:
- Automatic MCP availability checking
- Graceful fallback when MCP is unavailable
- Detailed error logging
- Status tracking

Example response when MCP is unavailable:
```json
{
  "response": "I'm sorry, but the Airbnb booking service is currently unavailable. Please try again later or contact support if the issue persists.",
  "status": "mcp_unavailable",
  "function_calls": null,
  "function_responses": null
}
```

## 🔍 Troubleshooting on Render

### 1. Check Debug Endpoint

After deploying to Render, check the debug endpoint:
```
https://your-app-name.onrender.com/debug
```

This will show you:
- Whether Node.js is available
- If MCP server can be accessed
- Environment variable status
- Any specific errors

### 2. Common Issues and Solutions

#### MCP Server Not Available
**Symptoms**: Debug endpoint shows `mcp_available: false`
**Solutions**:
- Check if Node.js is installed in Docker
- Verify npx is available
- Check Render logs for specific MCP errors
- Ensure MCP server package is accessible

#### API Key Issues
**Symptoms**: Google AI API errors
**Solutions**:
- Verify `GOOGLE_AI_API_KEY` is set in Render environment
- Check for trailing characters in API key
- Ensure service account JSON is complete

#### Timeout Issues
**Symptoms**: Requests timing out
**Solutions**:
- Check Gunicorn timeout settings
- Verify MCP server startup time
- Look for memory constraints in Render logs

### 3. Environment Variables for Render

Make sure these are set in your Render environment:

```bash
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}
ENVIRONMENT=production
```

### 4. Deployment Steps

1. **Deploy to Render** with the updated configuration
2. **Check the debug endpoint** on your Render URL
3. **Review Render logs** for any errors
4. **Test the MCP endpoint** with a simple request
5. **If issues persist**, check specific error messages from the debug endpoint

## 📊 Debug Output Examples

### Successful Debug Response
```json
{
  "status": "ok",
  "environment": {
    "environment": "production",
    "google_ai_api_key": "present",
    "google_cloud_credentials": "present",
    "working_directory": "/app",
    "python_executable": "/usr/local/bin/python"
  },
  "node": {
    "node_version": "v18.17.0",
    "npm_version": "9.6.7",
    "npx_version": "9.6.7"
  },
  "mcp": {
    "mcp_available": true
  },
  "mcp_global_available": true
}
```

### Failed Debug Response
```json
{
  "status": "ok",
  "environment": {
    "environment": "production",
    "google_ai_api_key": "present",
    "google_cloud_credentials": "present",
    "working_directory": "/app",
    "python_executable": "/usr/local/bin/python"
  },
  "node": {
    "node_version": "not_available",
    "npm_version": "not_available",
    "npx_version": "not_available"
  },
  "mcp": {
    "mcp_available": false,
    "mcp_error": "ENOENT: no such file or directory, stat 'node'"
  },
  "mcp_global_available": false
}
```

## 🎯 Next Steps

1. **Deploy the updated code** to Render
2. **Check the debug endpoint** immediately after deployment
3. **Review the output** for any issues
4. **Test the MCP endpoint** with a simple request
5. **If MCP is unavailable**, the system will provide a graceful fallback
6. **Monitor Render logs** for any additional errors

## 📞 Support

If you continue to experience issues:

1. **Check the debug endpoint** for specific error messages
2. **Review Render logs** for detailed error information
3. **Test endpoints individually** to isolate the problem
4. **Verify environment variables** are correctly set
5. **Check Node.js installation** in the Docker container

The enhanced debugging features should help identify and resolve the specific issues causing MCP problems on Render. 