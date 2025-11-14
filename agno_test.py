from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.youtube import YouTubeTools

agent = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyBfL4hHioC3-s96PCJf-IN5nxfn1fGZoGw"),
    tools=[YouTubeTools()],
        description="You are a YouTube agent. Obtain the captions of a YouTube video and answer questions.",
)

agent.print_response("Extract the full transcript from this video https://www.youtube.com/watch?v=4yU82_r0l0c", markdown=True)