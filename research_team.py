"""
Research Workflow for Personal Agents.

This file combines all 8 specialized agents into a coordinated Workflow with explicit Steps for phases, including a parallel research team.
"""

from agents.youtube_agent import create_youtube_agent
from agents.strategy_agent import create_strategy_agent
from agents.academic_agent import create_academic_agent
from agents.community_agent import create_community_agent
from agents.web_agent import create_web_agent
from agents.news_agent import create_news_agent
from agents.verification_agent import create_verification_agent
from agents.synthesis_agent import create_synthesis_agent
from config import get_db, check_agno_available

from textwrap import dedent
from agno.team import Team
from agno.workflow import Step, Workflow, Parallel

def create_research_workflow():
    """Create the complete 8-agent research workflow with explicit phases."""
    check_agno_available()

    db = get_db()

    # Create all agents
    youtube_agent = create_youtube_agent()
    strategy_agent = create_strategy_agent()
    academic_agent = create_academic_agent()
    community_agent = create_community_agent()
    web_agent = create_web_agent()
    news_agent = create_news_agent()
    verification_agent = create_verification_agent()
    synthesis_agent = create_synthesis_agent()

    # Define the workflow steps for controlled execution
    research_workflow = Workflow(
        name="Research Workflow",
        description="A sequential and parallel workflow for comprehensive research.",
        db=db,
        # Initialize shared state for the workflow
        session_state={
            "youtube_data": {},      # Store YouTube metadata and transcript
            "research_strategy": {},  # Store the research strategy
            "research_findings": {    # Store findings from each agent
                "academic": [],
                "community": [],
                "web": [],
                "news": []
            },
            "verified_facts": [],     # Store verified information
            "final_synthesis": {}     # Store the final synthesized report
        },
        add_session_state_to_context=True,  # Make state available in context
        enable_agentic_state=True,    # Enable automatic state updates
        steps=[
            # Phase 1: Sequential execution for initial analysis
            Step(
                name="Phase1_YouTube_Analysis",
                agent=youtube_agent,
                description="Extract metadata and transcript from a YouTube URL."
            ),
            # Phase 2: Sequential execution for planning
            Step(
                name="Phase2_Strategy_Planning",
                agent=strategy_agent,
                description="Create a research strategy based on the initial analysis."
            ),
            # Phase 3: Parallel execution for broad research
            Parallel(
                Step(name="Academic_Research", agent=academic_agent),
                Step(name="Community_Research", agent=community_agent),
                Step(name="Web_Research", agent=web_agent),
                Step(name="News_Research", agent=news_agent),
                name="Phase3_Parallel_Research",
                description="Execute academic, community, web, and news research in parallel."
            ),
            # Phase 4: Sequential execution for fact-checking
            Step(
                name="Phase4_Fact_Verification",
                agent=verification_agent,
                description="Fact-check the findings from the parallel research phase."
            ),
            # Phase 5: Sequential execution for final synthesis
            Step(
                name="Phase5_Research_Synthesis",
                agent=synthesis_agent,
                description="Synthesize all verified findings into a final report."
            ),
        ],
    )

    return research_workflow