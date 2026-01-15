from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from nodes import translator, reviewer

# --- State Definition ---
class AgentState(TypedDict):
    input_code: str
    source_lang: str
    target_lang: str
    generated_code: str
    errors: List[str]
    iterations: int

# --- Conditional Logic ---
def should_continue(state):
    errors = state.get('errors', [])
    iterations = state.get('iterations', 0)
    
    if errors and iterations < 3: # Max 3 retries
        return "translator"
    return END

# --- Graph Construction ---
def create_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("translator", translator)
    workflow.add_node("reviewer", reviewer)

    # Add Edges
    workflow.set_entry_point("translator")
    workflow.add_edge("translator", "reviewer")
    
    # Conditional Edge
    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "translator": "translator",
            END: END
        }
    )

    # Compile
    app = workflow.compile()
    return app
