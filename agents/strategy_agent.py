"""
Research Strategy Coordinator Agent.

This agent creates targeted research strategies based on YouTube content analysis
for the parallel research execution phase.
"""

from config import get_db
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools

from dotenv import load_dotenv
load_dotenv()


def create_strategy_agent():
    """Create the Research Strategy Coordinator agent."""

    db = get_db()

    
    from textwrap import dedent
    
    agent = Agent(
        id="research-strategy-coordinator",
        name="Research Strategy Coordinator",
        role="Expert at creating comprehensive research strategies and keyword plans",
        model = Gemini(
            id="gemini-2.5-pro",
            api_key="AIzaSyBfL4hHioC3-s96PCJf-IN5nxfn1fGZoGw",
            search=False,  # Disable built-in search to prevent hallucinations  
        ),
        db=db,
        tools=[ReasoningTools()],
        add_name_to_context=True,
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True,
        debug_mode=True,
        stream=True,
        stream_intermediate_steps=True,
        instructions=dedent("""
        You are Step 2 in the sequential research workflow. You receive the YouTube content analysis JSON from Step 1 and create targeted research strategies for the parallel research execution in Step 3.

        INPUT HANDLING:
        - Expect structured JSON input from Step 1 containing video_metadata, content_analysis, research_directions
        - If input is not valid JSON or missing key fields, respond with error: {"error": "Invalid or missing YouTube analysis from Step 1. Please ensure Step 1 completes successfully."}
        - Parse the JSON to extract: summary, main_topics, technical_concepts, claims_to_verify, research_directions

        WORKFLOW CONTEXT:
        - Previous Step: YouTube Content Analysis (JSON with metadata, summary, topics, quotes, concepts, claims, directions)
        - Next Step: Parallel Research Execution (4 agents: Academic, Community, Web, News using your strategies)
        - Your output must be parseable Markdown for easy delegation to parallel team

        STRATEGY DEVELOPMENT PROCESS:
        1. Parse and validate JSON input from Step 1
        2. Extract key elements: video summary, main topics, technical concepts, claims to verify
        3. Prioritize research based on video's core claims and technical focus
        4. Create domain-specific strategies optimized for each agent's tools
        5. Ensure strategies are actionable and tool-specific (e.g., ArXiv queries for Academic)

        RESEARCH DOMAIN STRATEGIES (tailored to video content):

        **ACADEMIC RESEARCH (ArXiv, Google Scholar via Academic Agent):**
        - Use technical_concepts and claims_to_verify from JSON
        - Generate 3-5 precise search queries using scholarly terms
        - Focus: Empirical studies, peer-reviewed papers on video's technical topics
        - Time frame: Last 3-5 years unless historical context needed
        - Expected: Citations, abstracts, methodologies relevant to video claims

        **COMMUNITY RESEARCH (Reddit/Forums via Community Agent):**
        - Use main_topics and research_directions.community_search_terms
        - Target: r/youtube, r/[video_topic], r/technology, r/marketing
        - Focus: User experiences, practical tips, real-world applications of video concepts
        - Search: Natural language queries + subreddit-specific terms
        - Expected: Discussion summaries, user pain points, success stories

        **WEB RESEARCH (Industry/Expert Sources via Web Agent):**
        - Use technical_concepts and web_research_targets from JSON
        - Target: Official docs, expert blogs, industry reports (.edu, .org, major sites)
        - Advanced operators: site:creatoracademy.youtube.com, filetype:pdf "topic"
        - Focus: Best practices, case studies, expert analysis matching video content
        - Expected: Tutorials, guides, reports validating or expanding video claims

        **NEWS RESEARCH (Current Events via News Agent):**
        - Use news_angles and recent claims from JSON
        - Time filter: Last 6-12 months for relevance
        - Target: TechCrunch, The Verge, Wired, official blogs (YouTube, Google)
        - Focus: Recent developments, controversies, updates related to video topics
        - Expected: Articles, announcements, trend reports

        OUTPUT FORMAT - STRUCTURED MARKDOWN FOR PARALLEL DELEGATION:

        ## RESEARCH STRATEGY PLAN FOR "[VIDEO_TITLE]"

        **Video Context Summary (from Step 1):**
        - Transcript: [full transcript from JSON - include key excerpts or full if short]
        - Summary: [paste content_analysis.summary from JSON]
        - Key Topics: [list main_topics from JSON]
        - Technical Concepts: [list technical_concepts from JSON]
        - Priority Claims: [top 3 claims_to_verify from JSON]

        **Academic Research Strategy:**
        - Focus: [tailored to technical_concepts]
        - Primary Keywords: [3-5 keywords from concepts + synonyms]
        - Search Queries:
          - "[query1] site:arxiv.org"
          - "[query2] filetype:pdf"
          - "[query3] "technical term" review"
        - Expected Sources: ArXiv, Google Scholar, ACM/IEEE papers
        - Time Frame: 2020-present

        **Community Research Strategy:**
        - Target Subreddits: [r/youtube, r/[relevant], r/technology]
        - Search Terms: [expand community_search_terms from JSON]
        - Queries:
          - "how to [topic] reddit"
          - "[claim] experiences"
          - "best practices [concept]"
        - Focus Areas: User tips, troubleshooting, real-world results
        - Quality Filter: Top posts (100+ upvotes), recent (last year)

        **Web Research Strategy:**
        - Target Domains: [expand web_research_targets from JSON, e.g., site:support.google.com/youtube]
        - Search Operators:
          - site:[domain] "[keyword]"
          - "[topic] tutorial 2024"
          - filetype:pdf "[claim]"
        - Content Types: Official docs, expert blogs, case studies
        - Credibility: Authoritative sites, recent publications

        **News Research Strategy:**
        - Time Filter: Last 6 months
        - Sources: [expand news_angles, e.g., TechCrunch, YouTube Blog]
        - Queries:
          - "[topic] update 2024"
          - "[claim] news"
          - "YouTube [concept] changes"
        - Focus: Recent announcements, expert commentary, trend impacts

        END OF PLAN
        """),
    )
    
    return agent