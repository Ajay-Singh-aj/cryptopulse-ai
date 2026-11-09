
from app.graph.workflow import crypto_pulse_workflow


def test_workflow_compiles():
    assert crypto_pulse_workflow is not None


def test_workflow_contains_all_nodes():
    graph = crypto_pulse_workflow.get_graph()

    expected_nodes = {
        "research",
        "relevance",
        "verification",
        "analysis",
        "newsletter",
    }

    assert expected_nodes.issubset(set(graph.nodes.keys()))
