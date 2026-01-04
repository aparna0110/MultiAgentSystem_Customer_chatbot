import os
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import tier1_node, tier2_node, manager_node
from graph.router import route_based_on_confidence


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("tier1", tier1_node)
    graph.add_node("tier2", tier2_node)
    graph.add_node("manager", manager_node)

    graph.set_entry_point("tier1")

    graph.add_conditional_edges(
        "tier1",
        route_based_on_confidence,
        {
            "tier2": "tier2",
            "manager": "manager",
        },
    )

    graph.add_edge("tier2", "manager")
    graph.add_edge("manager", END)

    compiled_graph = graph.compile()

    # 🔥 SAVE FLOW DIAGRAM HERE
    os.makedirs("graph", exist_ok=True)
    compiled_graph.get_graph().draw_mermaid_png(
        output_file_path="graph/agent_workflow.png"
    )

    return compiled_graph
