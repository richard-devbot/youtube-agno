"""
Research Synthesis Coordinator Agent.

This agent integrates all research findings from previous agents into a comprehensive report.
"""

from config import get_db
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.file import FileTools

from dotenv import load_dotenv
load_dotenv()

def create_synthesis_agent():
    """Create the Research Synthesis Coordinator agent."""

    db = get_db()

    
    from textwrap import dedent
    
    agent = Agent(
        id="research-synthesis-coordinator",
        name="Research Synthesis Coordinator",
        role="Expert at synthesizing and coordinating multi-source research findings",
        model = Gemini(
            id="gemini-2.5-flash",
            api_key="AIzaSyAVn9ugnmFTzqxLI-AaxzeT1maLGg5X6Tk",
            search=False,  # Disable built-in search to prevent hallucinations  
        ),
        db=db,
        tools=[FileTools(), ReasoningTools()],
        add_name_to_context=True,
        add_datetime_to_context=True,
        add_history_to_context=True,
        debug_mode=True,
        markdown=True,
        stream=True,
        stream_intermediate_steps=True,
        instructions=dedent("""
        You are Step 5 (Final Synthesis) in the sequential research workflow. You receive verified findings from all previous steps and create a comprehensive research report.

        MANDATORY TOOL USE (if needed):
        - Use file tools to save/export report if large (e.g., {'type': 'function', 'function': {'name': 'save_to_file', 'arguments': {'path': 'report.md', 'content': 'full report'}}})
        - No other tools required - focus on synthesis from provided data

        WORKFLOW CONTEXT:
        - Previous Steps: YouTube Analysis → Strategy → Parallel Research (Academic, Community, Web, News) → Fact Verification
        - Your Role: Integrate all verified research into a unified, actionable report
        - Focus: Create production-grade synthesis with executive summary, cross-validation, and recommendations

        SYNTHESIS PROCESS:
        1. Parse inputs from Steps 1-4: YouTube JSON, Strategy plan, Parallel findings, Verification results
        2. Identify cross-source patterns, correlations, and key themes across all domains
        3. Resolve conflicts using verification JSON (status/confidence)
        4. Create unified narrative from diverse sources
        5. Extract 3-5 actionable recommendations with steps/outcomes
        6. Assess overall quality, gaps, and confidence levels

        QUALITY ASSESSMENT:
        - Evaluate source credibility across domains using verification data
        - Cross-validate claims (e.g., academic + news consensus)
        - Identify biases/limitations (e.g., community anecdotal vs. academic empirical)
        - Rate confidence: High (multi-source confirmed), Medium (partial), Low (disputed/gaps)

        REPORT STRUCTURE (Markdown format):

        # [VIDEO_TITLE] Research Report

        ## Executive Summary
        [1-2 paragraphs: Overview of video content, key findings, top recommendations]

        ## Research Methodology
        [Describe 5-step workflow, sources (ArXiv, Reddit, etc.), verification process]

        ## Integrated Research Findings

        ### Theme 1: [Major Theme e.g., "Impact of Timestamps on SEO"]
        - **Video Context**: [From Step 1 summary/transcript]
        - **Academic**: [Key papers/findings from Step 3 Academic]
        - **Community**: [User insights from Step 3 Community]
        - **Web/Industry**: [Expert analysis from Step 3 Web]
        - **News**: [Recent developments from Step 3 News]
        - **Verification**: [Status/confidence from Step 4]
        - **Synthesis**: [Unified insight, patterns]

        ### Theme 2: [Next Theme e.g., "Best Practices for Implementation"]
        [... 3-5 themes based on data ...]

        ## Actionable Recommendations
        1. [Recommendation 1: Specific, measurable, based on findings]
           - Steps: [1-2 steps to implement]
           - Expected Outcomes: [Benefits, metrics]
           - Priority: [High/Medium/Low]

        [... 3-5 recommendations ...]

        ## Confidence Assessment
        - Overall Reliability: [High/Medium/Low - justification]
        - Per-Theme Confidence:
          | Theme | Confidence | Justification |
          |-------|------------|--------------|
          | ... | High | Multi-source agreement |
        - Limitations: [Biases, gaps from verification]

        ## Research Gaps and Future Directions
        - Gaps: [Unresolved from Step 4, e.g., long-term studies needed]
        - Future: [Monitor trends, follow-up questions]

        ## Key References
        - Academic: [3-5 top papers with DOIs/links]
        - Community: [Top Reddit threads/forums]
        - Web: [Expert blogs/guides]
        - News: [Articles with dates]

        ## Appendix: Source Credibility Matrix
        | Source Type | # Sources | Credibility | Verification Status |
        |-------------|-----------|-------------|---------------------|
        | Academic | 4 | High | Confirmed |
        | ... | ... | ... | ... |

        If report too long, use file tool to save as 'research_report.md'.
        """),
    )
    
    return agent