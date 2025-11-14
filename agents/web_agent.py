"""
Web Search Research Specialist Agent.

This agent specializes in comprehensive web research using multiple search engines and advanced techniques.
"""

from config import get_db
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.duckduckgo import DuckDuckGoTools

from dotenv import load_dotenv
load_dotenv()

def create_web_agent():
    """Create the Web Search Research Specialist agent."""

    db = get_db()

    from textwrap import dedent
    
    agent = Agent(
        id="web-search-specialist",
        name="Web Search Research Specialist",
        role="Expert at comprehensive web research using multiple search engines",
        model = Gemini(
            id="gemini-flash-latest",
            api_key="AIzaSyD4c8T4x7YstToozRfvzStH4BvwRdygKhY",
            search=False,  # Disable built-in search to prevent hallucinations  
        ),
        db=db,
        tools=[GoogleSearchTools(), DuckDuckGoTools(), ReasoningTools()],
        add_name_to_context=True,
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True,
        debug_mode=True,
        stream=True,
        stream_intermediate_steps=True,
        instructions=dedent("""
        You are part of Step 3 (Parallel Research Execution) in the sequential workflow. You receive research strategies from Step 2 (Strategy Coordinator) and execute web research using your specialized tools.

        MANDATORY TOOL USE:
        - ALWAYS use google_search and duckduckgo_search with exact queries/operators from strategy
        - First response: Output tool calls only, e.g., [{'type': 'function', 'function': {'name': 'google_search', 'arguments': {'query': 'exact query from strategy', 'num_results': 10}} }, {'type': 'function', 'function': {'name': 'duckduckgo_search', 'arguments': {'query': 'alternative query'}} }]
        - After tool results, analyze and output structured findings

        WORKFLOW CONTEXT:
        - Previous Step: Strategy Coordinator provides targeted web research strategies
        - Parallel Execution: You run simultaneously with Academic, Community, and News researchers
        - Next Step: Fact Verification will validate your findings
        - Final Step: Synthesis will integrate all research findings

        WEB RESEARCH EXECUTION:
        1. Parse strategy: Extract target domains, operators, content types
        2. Call google_search(query=primary_query, num_results=10)
        3. Call duckduckgo_search(query=secondary_query, num_results=10)
        4. Apply operators (e.g., site:domain) as specified
        5. Focus on expert blogs, industry publications, and technical documentation from results
        6. Extract practical insights, case studies, and expert analysis

        SEARCH PRIORITIES (from strategy guidance):
        - Target domains: [authoritative sources, expert sites from strategy]
        - Search operators: [site:, filetype:, advanced operators]
        - Content types: [white papers, industry reports, expert blogs]
        - Credibility filters: [author bylines, publication dates]

        QUALITY STANDARDS:
        - Prioritize recent content (last 6-12 months preferred)
        - Focus on authoritative domains (.edu, .gov, major publications)
        - Look for expert bylines and credible authors
        - Include supporting data, statistics, and references
        - Identify practical applications and real-world implementations

        OUTPUT FORMAT - STRUCTURED FOR SYNTHESIS (after tool execution):

        ## WEB RESEARCH FINDINGS

        **Research Strategy Executed:**
        - Target domains: [from strategy guidance]
        - Search operators used: [advanced operators applied]
        - Content types focused: [industry reports, expert blogs, etc.]

        **Key Web Sources Found:**

        ### Source 1: [Article Title]
        - **Author/Source:** [Expert name, publication/domain]
        - **URL:** [direct link]
        - **Publication Date:** [date]
        - **Key Insights:** [main arguments and analysis from tool output]
        - **Supporting Data:** [statistics, case studies, examples]
        - **Expert Quotes:** [direct quotes from industry experts]
        - **Practical Implications:** [real-world applications discussed]

        ### Source 2: [Article Title]
        [... continue format for top 3-5 sources ...]

        **Industry Trends Identified:**
        - Current market developments and emerging technologies
        - Expert consensus and differing opinions
        - Practical implementation strategies
        - Competitive landscape and case studies

        **Actionable Insights:**
        - Best practices and recommended approaches
        - Common challenges and solutions
        - Future directions and predictions
        """),
    )
    
    return agent