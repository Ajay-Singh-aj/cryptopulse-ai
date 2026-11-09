
from langgraph.graph import StateGraph, START, END

from app.graph.state import CryptoPulseState
from app.graph.nodes import (
    research_node,
    relevance_node,
    verification_node,
    analysis_node,
    newsletter_node,
)
from app.graph.edges import (
    should_continue_after_research,
    should_continue_after_verification,
)


def build_workflow():
    """Build and compile the CryptoPulse AI LangGraph workflow."""

    workflow = StateGraph(CryptoPulseState)

    # Register nodes
    workflow.add_node("research", research_node)
    workflow.add_node("relevance", relevance_node)
    workflow.add_node("verification", verification_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("newsletter", newsletter_node)

    # Define execution order
    workflow.add_edge(START, "research")

    workflow.add_conditional_edges(
        "research",
        should_continue_after_research,
        {
            "relevance": "relevance",
            END: END,
        },
    )

    workflow.add_edge("relevance", "verification")

    workflow.add_conditional_edges(
        "verification",
        should_continue_after_verification,
        {
            "analysis": "analysis",
            END: END,
        },
    )

    workflow.add_edge("analysis", "newsletter")
    workflow.add_edge("newsletter", END)

    return workflow.compile()


# Ready-to-use compiled workflow
crypto_pulse_workflow = build_workflow()
