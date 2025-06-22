"""
FastAPI application for Travel Concierge Agent
"""

import os
import asyncio
import uuid
import json
import subprocess
from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime

from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai.types import Content, Part
from travel_concierge.agent import root_agent
from travel_concierge.sub_agents.booking.agent import booking_agent
from travel_concierge.shared_libraries import constants

# Load environment variables
load_dotenv()

# Debug environment at startup
def debug_environment():
    """Debug environment variables and system setup"""
    print("🔍 DEBUGGING ENVIRONMENT SETUP")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"Google AI API Key present: {'Yes' if os.getenv('GOOGLE_AI_API_KEY') else 'No'}")
    print(f"Google Cloud Credentials present: {'Yes' if os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON') else 'No'}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python executable: {os.sys.executable}")
    
    # Check Node.js availability
    try:
        node_result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        print(f"Node.js version: {node_result.stdout.strip() if node_result.returncode == 0 else 'Not available'}")
    except Exception as e:
        print(f"Node.js check failed: {e}")
    
    # Check npm availability
    try:
        npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
        print(f"npm version: {npm_result.stdout.strip() if npm_result.returncode == 0 else 'Not available'}")
    except Exception as e:
        print(f"npm check failed: {e}")
    
    # Check npx availability
    try:
        npx_result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=5)
        print(f"npx version: {npx_result.stdout.strip() if npx_result.returncode == 0 else 'Not available'}")
    except Exception as e:
        print(f"npx check failed: {e}")
    
    # Check if MCP server is globally installed
    try:
        mcp_result = subprocess.run(['npx', '-y', '@openbnb/mcp-server-airbnb', '--help'], 
                                  capture_output=True, text=True, timeout=10)
        print(f"MCP server available: {'Yes' if mcp_result.returncode == 0 else 'No'}")
        if mcp_result.stderr:
            print(f"MCP server error: {mcp_result.stderr[:200]}...")
    except Exception as e:
        print(f"MCP server check failed: {e}")
    
    print("🔍 END DEBUGGING")

# Run environment debug at startup
debug_environment()

# Set up Google Cloud authentication for production
def setup_google_auth():
    """Set up Google Cloud authentication for production deployment"""
    # Check if we have service account JSON in environment
    credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if credentials_json:
        try:
            # Parse the JSON and write to a temporary file
            credentials_data = json.loads(credentials_json)
            credentials_path = '/tmp/google-credentials.json'
            with open(credentials_path, 'w') as f:
                json.dump(credentials_data, f)
            
            # Set the environment variable to point to the file
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            print("✅ Google Cloud authentication configured from environment")
        except Exception as e:
            print(f"⚠️ Warning: Failed to set up Google Cloud credentials: {e}")
    else:
        print("ℹ️ Using default Google Cloud authentication")

# Initialize Google Cloud authentication
setup_google_auth()

# Create FastAPI app
app = FastAPI(
    title="Travel Concierge API",
    description="AI-powered travel concierge service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize session service
session_service = InMemorySessionService()

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

class MCPAirbnbRequest(BaseModel):
    message: str

class MCPAirbnbResponse(BaseModel):
    response: str
    status: str = "success"
    function_calls: Optional[list] = None
    function_responses: Optional[list] = None

# Global variable to store MCP tools and exit stack
mcp_tools = None
mcp_exit_stack = None
mcp_available = True  # Track MCP availability

async def check_mcp_availability():
    """Check if MCP server is available and working"""
    global mcp_available
    try:
        # Test MCP server availability
        result = subprocess.run(
            ['npx', '-y', '@openbnb/mcp-server-airbnb', '--help'],
            capture_output=True,
            text=True,
            timeout=15
        )
        mcp_available = result.returncode == 0
        print(f"🔍 MCP availability check: {'Available' if mcp_available else 'Not available'}")
        if not mcp_available and result.stderr:
            print(f"🔍 MCP error: {result.stderr[:300]}...")
        return mcp_available
    except Exception as e:
        print(f"🔍 MCP availability check failed: {e}")
        mcp_available = False
        return False

async def get_mcp_tools_async():
    """Gets tools from Airbnb MCP Server with comprehensive error handling."""
    global mcp_tools, mcp_exit_stack, mcp_available
    
    # Check MCP availability first
    if not await check_mcp_availability():
        print("⚠️ MCP server not available, returning empty tools")
        return [], None
    
    if mcp_tools is None:
        try:
            print("🔧 Setting up Airbnb MCP Server...")
            mcp_toolset = MCPToolset(
                connection_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
                )
            )
            mcp_tools = await mcp_toolset.get_tools()
            mcp_exit_stack = mcp_toolset
            print(f"✅ Airbnb MCP Server connected with {len(mcp_tools) if mcp_tools else 0} tools")
            
            # Debug tool names
            if mcp_tools:
                tool_names = [getattr(tool, 'name', 'unnamed') for tool in mcp_tools]
                print(f"🔍 Available MCP tools: {tool_names}")
            
        except Exception as e:
            print(f"❌ Failed to set up MCP server: {e}")
            mcp_available = False
            mcp_tools = []
            mcp_exit_stack = None
    
    return mcp_tools or [], mcp_exit_stack

def find_agent(agent, target_name):
    """A convenient function to find an agent from an existing agent graph."""
    result = None
    if agent.name == target_name:
        return agent
    for sub_agent in agent.sub_agents:
        result = find_agent(sub_agent, target_name)
        if result:
            break
    for tool in agent.tools:
        if isinstance(tool, AgentTool):
            result = find_agent(tool.agent, target_name)
            if result:
                break
    return result

async def get_agent_with_mcp_async():
    """Creates an ADK Agent with tools from Airbnb MCP Server."""
    tools, exit_stack = await get_mcp_tools_async()
    
    if not tools:
        print("⚠️ No MCP tools available, proceeding without MCP")
        return root_agent, None
    
    print(f"🔧 Inserting {len(tools)} Airbnb MCP tools into Travel-Concierge...")
    planner = find_agent(root_agent, "planning_agent")
    if planner:
        print(f"✅ Found {planner.name}, adding MCP tools")
        # Clear existing MCP tools to avoid duplicates
        planner.tools = [tool for tool in planner.tools if not hasattr(tool, 'name') or not tool.name.startswith('airbnb_')]
        planner.tools.extend(tools)
        print(f"✅ Added {len(tools)} MCP tools to planner")
    else:
        print("⚠️ planning_agent not found")
    
    return root_agent, exit_stack

@app.post("/mcp-airbnb", response_model=MCPAirbnbResponse)
async def mcp_airbnb(request: MCPAirbnbRequest):
    """Send a message to the travel concierge agent with Airbnb MCP tools enabled"""
    try:
        print(f"🔍 Processing MCP request: {request.message[:100]}...")
        
        # Check MCP availability first
        if not mcp_available:
            print("⚠️ MCP not available, providing fallback response")
            return MCPAirbnbResponse(
                response="I'm sorry, but the Airbnb booking service is currently unavailable. Please try again later or contact support if the issue persists.",
                status="mcp_unavailable"
            )
        
        # Generate unique session and user IDs for each request
        session_id = str(uuid.uuid4())
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # Create session in session service
        await session_service.create_session(
            app_name="travel-concierge",
            user_id=user_id,
            session_id=session_id
        )
        
        # Create content from message
        content = Content(
            parts=[Part.from_text(text=request.message)],
            role="user"
        )
        
        # Get agent with MCP tools
        agent, exit_stack = await get_agent_with_mcp_async()
        
        # Create runner for this request
        runner = Runner(
            app_name="travel-concierge",
            agent=agent,
            session_service=session_service
        )
        
        # Run the agent and collect response
        response_text = ""
        function_calls = []
        function_responses = []
        
        try:
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            ):
                # Extract text from events
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                response_text += part.text
                            if part.function_call:
                                function_calls.append({
                                    "name": part.function_call.name,
                                    "args": part.function_call.args
                                })
                            if part.function_response:
                                function_responses.append({
                                    "name": part.function_response.name,
                                    "response": part.function_response.response
                                })
                    elif hasattr(event.content, 'text'):
                        response_text += event.content.text
        except Exception as e:
            print(f"❌ Error during agent execution: {e}")
            response_text = f"I encountered an error while processing your request: {str(e)}. Please try again."
        
        # If no response text was collected, provide a default response
        if not response_text.strip():
            response_text = "I'm processing your request. Please try again."
        
        print(f"✅ MCP request completed successfully")
        return MCPAirbnbResponse(
            response=response_text,
            status="success",
            function_calls=function_calls if function_calls else None,
            function_responses=function_responses if function_responses else None
        )
        
    except Exception as e:
        print(f"❌ MCP endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the travel concierge agent"""
    try:
        # Generate unique session and user IDs for each request
        session_id = str(uuid.uuid4())
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # Create session in session service
        await session_service.create_session(
            app_name="travel-concierge",
            user_id=user_id,
            session_id=session_id
        )
        
        # Create content from message
        content = Content(
            parts=[Part.from_text(text=request.message)],
            role="user"
        )
        
        # Create runner
        runner = Runner(
            app_name="travel-concierge",
            agent=root_agent,
            session_service=session_service
        )
        
        # Run the agent and collect response
        response_text = ""
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            # Extract text from events
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
                elif hasattr(event.content, 'text'):
                    response_text += event.content.text
        
        # If no response text was collected, provide a default response
        if not response_text.strip():
            response_text = "I'm processing your request. Please try again."
        
        return ChatResponse(response=response_text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@app.get("/debug")
async def debug_endpoint():
    """Debug endpoint to check system status"""
    try:
        # Check environment variables
        env_status = {
            "environment": os.getenv('ENVIRONMENT', 'development'),
            "google_ai_api_key": "present" if os.getenv('GOOGLE_AI_API_KEY') else "missing",
            "google_cloud_credentials": "present" if os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON') else "missing",
            "working_directory": os.getcwd(),
            "python_executable": os.sys.executable
        }
        
        # Check Node.js
        node_status = {}
        try:
            node_result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
            node_status["node_version"] = node_result.stdout.strip() if node_result.returncode == 0 else "not_available"
        except Exception as e:
            node_status["node_version"] = f"error: {str(e)}"
        
        # Check npm
        try:
            npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
            node_status["npm_version"] = npm_result.stdout.strip() if npm_result.returncode == 0 else "not_available"
        except Exception as e:
            node_status["npm_version"] = f"error: {str(e)}"
        
        # Check npx
        try:
            npx_result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=5)
            node_status["npx_version"] = npx_result.stdout.strip() if npx_result.returncode == 0 else "not_available"
        except Exception as e:
            node_status["npx_version"] = f"error: {str(e)}"
        
        # Check MCP server
        mcp_status = {}
        try:
            mcp_result = subprocess.run(['npx', '-y', '@openbnb/mcp-server-airbnb', '--help'], 
                                      capture_output=True, text=True, timeout=10)
            mcp_status["mcp_available"] = mcp_result.returncode == 0
            if mcp_result.stderr:
                mcp_status["mcp_error"] = mcp_result.stderr[:200]
        except Exception as e:
            mcp_status["mcp_available"] = False
            mcp_status["mcp_error"] = str(e)
        
        return {
            "status": "ok",
            "environment": env_status,
            "node": node_status,
            "mcp": mcp_status,
            "mcp_global_available": mcp_available
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "travel-concierge-api"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Travel Concierge API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "mcp_airbnb": "/mcp-airbnb",
            "health": "/health",
            "debug": "/debug"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 