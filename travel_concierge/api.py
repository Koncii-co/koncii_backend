"""FastAPI application for Travel Concierge Agent"""

import os
import asyncio
import uuid
import json
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

app = FastAPI()

# CORS middleware setup (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session and artifact services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

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

async def get_mcp_tools_async():
    """Gets tools from Airbnb MCP Server."""
    global mcp_tools, mcp_exit_stack
    if mcp_tools is None:
        print("Setting up Airbnb MCP Server...")
        mcp_toolset = MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
            )
        )
        mcp_tools = await mcp_toolset.get_tools()
        mcp_exit_stack = mcp_toolset
        print("✅ Airbnb MCP Server connected")
    return mcp_tools, mcp_exit_stack

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
    print("Inserting Airbnb MCP tools into Travel-Concierge...")
    planner = find_agent(root_agent, "planning_agent")
    if planner:
        print(f"✅ Found {planner.name}, adding MCP tools")
        # Clear existing MCP tools to avoid duplicates
        planner.tools = [tool for tool in planner.tools if not hasattr(tool, 'name') or not tool.name.startswith('airbnb_')]
        planner.tools.extend(tools)
    else:
        print("⚠️ planning_agent not found")
    return root_agent, exit_stack

@app.post("/mcp-airbnb", response_model=MCPAirbnbResponse)
async def mcp_airbnb(request: MCPAirbnbRequest):
    """Send a message to the travel concierge agent with Airbnb MCP tools enabled"""
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
        
        # If no response text was collected, provide a default response
        if not response_text.strip():
            response_text = "I'm processing your request. Please try again."
        
        return MCPAirbnbResponse(
            response=response_text,
            status="success",
            function_calls=function_calls if function_calls else None,
            function_responses=function_responses if function_responses else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the travel concierge agent"""
    # ...existing code for chat endpoint...
    pass

@app.get("/")
async def root():
    return {
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "chat": "/chat",
        "mcp-airbnb": "/mcp-airbnb"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=