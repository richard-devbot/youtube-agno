"""
YouTube Content Analyst Agent (Pydantic-Enforced).

This agent uses a strict Pydantic output schema to ensure reliable,
structured data extraction, eliminating hallucination and guaranteeing
workflow compatibility.
"""
from textwrap import dedent

# Import core configuration and the specific Pydantic model for the output
from config import get_db
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.youtube import YouTubeTools

from dotenv import load_dotenv
load_dotenv()

def create_youtube_agent():
    """Create the YouTube Content Analyst agent with a Pydantic output schema."""
    db = get_db()
    agent = Agent(
        id="youtube-content-analyst",
        name="YouTube Content Analyst",
        role="A specialist bot for extracting and structuring YouTube data into a Pydantic schema.",
        model = Gemini(
            id="gemini-2.5-pro",
            api_key="AIzaSyD4c8",
            search=False,  # Disable built-in search to prevent hallucinations  
        ),
        db=db,
        markdown=True,
        debug_mode=True,
        tools=[YouTubeTools()],
        instructions=dedent("""
        **OPERATIONAL MANDATE: You are a data processing service. Your only function is to populate a `YoutubeAnalysisOutput` Pydantic schema using the provided tools.**

        **PRIMARY DIRECTIVE: TOOL USE IS MANDATORY**
        - You are forbidden from using general web search or your internal knowledge.
        - Your ONLY source of data is the output of the `get_youtube_video_data` and `get_youtube_video_captions` tools.
        - Your first response MUST be to call these tools with the URL from the input.

        **PROTOCOL:**
        1.  **Extract URL:** Identify the first valid YouTube URL from the user's input.
        2.  **Execute Tools:** Call `get_youtube_video_data(url=...)` and `get_youtube_video_captions(url=...)`.
        3.  **Map to Schema:** Use the data returned from the tools to populate ALL fields of the `YoutubeAnalysisOutput` schema.
            -   `video_id`: Extract the ID from the URL.
            -   `title`: Use the 'title' from `get_youtube_video_data`.
            -   `channel`: Use the 'author_name' from `get_youtube_video_data`.
            -   `description_key_points`: Read the full description from the tool and summarize it into a list of key bullet points.
            -   `main_topics`, `key_quotes`, `technical_concepts`, `claims_to_verify`: Derive these exclusively from the transcript returned by `get_youtube_video_captions`. If the transcript is unavailable, these lists must be empty.
            -   `research_directions`: Generate these based on the available topics and concepts.
        4.  **Handle Missing Data:** If `get_youtube_video_captions` returns an error or "No captions found", all transcript-dependent fields (like `main_topics`, `key_quotes`, etc.) MUST be empty lists (`[]`). Do not invent content.

        **Your entire goal is to produce a valid `YoutubeAnalysisOutput` object. Begin.**
        """),
        expected_output="A single, valid JSON object that strictly conforms to the `YoutubeAnalysisOutput` Pydantic schema.",
    )
    
    return agent
