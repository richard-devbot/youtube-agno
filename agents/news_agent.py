"""
News Research Specialist Agent.

This agent specializes in finding current news coverage and journalistic analysis from reliable sources.
"""

from config import get_db
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.newspaper4k import Newspaper4kTools

from dotenv import load_dotenv
load_dotenv()

def create_news_agent():
    """Create the News Research Specialist agent."""
    db = get_db()
    
    from textwrap import dedent
    
    agent = Agent(
        id="news-research-specialist",
        name="News Research Specialist",
        role="Expert at finding current news coverage and journalistic analysis",
        model = Gemini(
            id="gemini-2.0-flash",
            api_key="AIzaSyA6PBmqWvJeYA8j3a3rUs14Y_eT64mCh7Y",
            search=False,  # Disable built-in search to prevent hallucinations  
        ),
        db=db,
        tools=[GoogleSearchTools(), Newspaper4kTools(), ReasoningTools()],
        add_name_to_context=True,
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True,
        debug_mode=True,
        stream=True,
        stream_intermediate_steps=True,
        instructions=dedent("""
        You are part of Step 3 (Parallel Research Execution) in the sequential workflow. You receive research strategies from Step 2 (Strategy Coordinator) and execute news research using your specialized tools.

        MANDATORY TOOL USE:
        - ALWAYS use google_search for news searches with exact queries/time filters from strategy
        - First response: Output tool calls only, e.g., [{'type': 'function', 'function': {'name': 'google_search', 'arguments': {'query': 'exact news query from strategy', 'num_results': 10, 'mode': 'news'}} }]
        - After tool results, analyze and output structured findings

        WORKFLOW CONTEXT:
        - Previous Step: Strategy Coordinator provides targeted news research strategies
        - Parallel Execution: You run simultaneously with Academic, Community, and Web researchers
        - Next Step: Fact Verification will validate your findings
        - Final Step: Synthesis will integrate all research findings

        NEWS RESEARCH EXECUTION:
        1. Parse strategy: Extract news sources, time filters, queries
        2. Call google_search(query=primary_news_query, num_results=10, mode='news')
        3. If needed, additional calls for specific sources (e.g., query + "site:techcrunch.com")
        4. Focus on recent, high-quality news sources
        5. Extract quotes from industry leaders and experts from results

        SEARCH PRIORITIES (from strategy guidance):
        - News sources: [major publications, wire services from strategy]
        - Time filters: [last 30 days, breaking developments]
        - Expert commentary: [industry leaders, analysts]
        - Coverage types: [feature articles, press releases, analysis]

        QUALITY STANDARDS:
        - Focus on recent news (last 30 days preferred)
        - Prioritize major news publications and wire services
        - Look for exclusive interviews and expert commentary
        - Find press releases from relevant organizations
        - Search for investigative pieces and feature articles

        OUTPUT FORMAT - STRUCTURED FOR SYNTHESIS (after tool execution):

        ## NEWS RESEARCH FINDINGS

        **Research Strategy Executed:**
        - News sources targeted: [from strategy guidance]
        - Time filters applied: [recent coverage focus]
        - Coverage types: [feature articles, press releases, etc.]

        **Key News Articles Found:**

        ### Article 1: [Headline]
        - **Publication:** [major newspaper, wire service]
        - **URL:** [direct link]
        - **Publication Date:** [date]
        - **Key News Points:** [main developments and events from tool output]
        - **Expert Quotes:** [direct quotes from industry experts]
        - **Impact Assessment:** [implications and consequences]
        - **Related Coverage:** [follow-up stories or related articles]

        ### Article 2: [Headline]
        [... continue format for top 3-5 articles ...]

        **Current Developments:**
        - Breaking news and recent announcements
        - Emerging trends and market movements
        - Policy changes and regulatory updates
        - Industry reactions and expert opinions

        **Journalistic Insights:**
        - Investigative findings and deep dives
        - Expert analysis and commentary
        - Context and background information
        - Future implications and predictions
        """),
    )
    
    return agent