from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from nodes import query_optimizer, information_retrieval, content_scraper, information_synthesizer, report_generator

# --- State Definition ---
class AgentState(TypedDict):
    company: str
    queries: List[str]
    search_results: List[dict]
    urls: List[str]
    scraped_content: str
    synthesis: str
    report: str

# --- Graph Construction ---
def create_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("query_optimizer", query_optimizer)
    workflow.add_node("information_retrieval", information_retrieval)
    workflow.add_node("content_scraper", content_scraper)
    workflow.add_node("information_synthesizer", information_synthesizer)
    workflow.add_node("report_generator", report_generator)

    # Add Edges
    workflow.set_entry_point("query_optimizer")
    workflow.add_edge("query_optimizer", "information_retrieval")
    workflow.add_edge("information_retrieval", "content_scraper")
    workflow.add_edge("content_scraper", "information_synthesizer")
    workflow.add_edge("information_synthesizer", "report_generator")
    workflow.add_edge("report_generator", END)

    # Compile
    app = workflow.compile()
    return app
