"""
Standalone AG-UI Server for Personal Agents Research Workflow.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
import re
import json
from dotenv import load_dotenv

load_dotenv()

from agno.os.app import AgentOS
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# Import the research workflow and middleware
from research_team import create_research_workflow
from middleware.rate_limit import AdaptiveRateLimitMiddleware

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the research workflow
research_workflow = create_research_workflow()

# Setup AgentOS with the workflow
agent_os = AgentOS(
    workflows=[research_workflow],
)
app = agent_os.get_app()

# Add rate limiting middleware
app.add_middleware(
    AdaptiveRateLimitMiddleware,
    requests_per_minute=10,# Adjust based on Gemini's limits
    max_backoff_time=60,    # Maximum backoff of 60 seconds
    min_backoff_time=2      # Start with 2 second backoff
)

def extract_youtube_url(text: str) -> str:
    """Extract the first valid YouTube URL from a block of text."""
    # This regex is robust for various YouTube URL formats.
    youtube_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})"
    match = re.search(youtube_pattern, text)
    if match:
        # Return the full, clean URL for the agent to process.
        return f"https://www.youtube.com/watch?v={match.group(1)}"
    return None

@app.post("/agui")
@app.post("/research") # This endpoint can share the same logic
async def research_endpoint(request: Request):
    """
    Unified and corrected endpoint for AGUI and direct research.
    It intelligently extracts a YouTube URL and provides a clean,
    unambiguous input to the research workflow.
    Maintains session state for persistent research context.
    """
    try:
        body = await request.body()
        data = json.loads(body)
        
        # Standardize getting the user's content from various possible keys
        user_content = data.get('query') or data.get('content') or data.get('text') or data.get('message')
        
        if not user_content:
            raise HTTPException(status_code=400, detail="Request body must contain 'query' or 'content'.")
        
        logger.info(f"🔍 Received user content: \"{user_content}\"")
        
        # --- CRITICAL FIX: URL Extraction and Input Simplification ---
        youtube_url = extract_youtube_url(user_content)
        
        workflow_input = user_content
        if youtube_url:
            # If a URL is found, the workflow's input becomes JUST the URL.
            # This gives the youtube_agent a clean, direct task and prevents confusion.
            workflow_input = youtube_url
            logger.info(f"✓ YouTube URL extracted. Setting workflow input to: \"{workflow_input}\"")
        else:
            # If no URL is found, we assume the user provided a research topic.
            # The workflow will proceed with the original text.
            logger.warning(f"⚠ No YouTube URL found. Proceeding with text-based topic research.")

        # Generate a session ID based on user content or use provided one
        session_id = data.get('session_id', f"research_{hash(user_content)}")
        
        # Run the workflow with the clean, determined input and session management
        response = research_workflow.run(
            workflow_input,
            session_id=session_id,
            user_id=data.get('user_id', 'default_user')
        )
        
        # Get the current session state
        session_state = research_workflow.get_session_state()
        
        return {
            "status": "success",
            "query": user_content,
            "detected_youtube_url": youtube_url, # Return for context
            "session_id": session_id,
            "response": response.content if hasattr(response, 'content') else str(response),
            "session_state": session_state  # Return current state for client reference
        }
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid JSON in request body", "type": "invalid_json"}
        )
    except Exception as e:
        logger.error(f"Error in research endpoint: {e}", exc_info=True)
        
        # Handle rate limit errors specifically
        error_message = str(e)
        if "429" in error_message or "Too Many Requests" in error_message:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded from Gemini API",
                    "type": "gemini_rate_limit",
                    "retry_after": 30  # Suggest retry after 30 seconds for Gemini limits
                }
            )
            
        return JSONResponse(
            status_code=500,
            content={"detail": str(e), "type": "internal_error"}
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "workflow": "research_workflow"}

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "service": "Personal Agents Research Workflow",
        "version": "1.1",
        "endpoints": {
            "/research": "POST - Direct research endpoint (accepts JSON with 'query' or 'content')",
            "/agui": "POST - AGUI protocol endpoint (same as /research)",
            "/health": "GET - Health check"
        }
    }

def main():
    """Main function to setup and run the research workflow server."""
    print("🚀 Starting Personal Agents Research Workflow Server (v1.1 - Corrected)")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)

if __name__ == "__main__":
    main()