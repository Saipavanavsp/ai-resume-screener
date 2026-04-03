from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.classifier_agent import classifier_node
from app.agents.screener_agent import screener_node
from app.agents.researcher_agent import researcher_node
from app.agents.analyst_agent import analyst_node

def should_continue(state: AgentState):
    """Routing function after classification."""
    if state["is_valid_resume"]:
        return "screener"
    return END

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("classifier", classifier_node)
workflow.add_node("screener", screener_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)

# Add Edges
workflow.set_entry_point("classifier")
workflow.add_conditional_edges("classifier", should_continue, {"screener": "screener", END: END})
workflow.add_edge("screener", "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", END)

# Compile
app_graph = workflow.compile()

def run_resume_batch_workflow(file_name: str, resume_text: str, job_description: str):
    initial_state = {
        "file_name": file_name,
        "resume_text": resume_text,
        "job_description": job_description,
        "is_valid_resume": False,
        "rejection_reason": "",
        "extracted_profile": {},
        "research_results": "",
        "final_swot": "",
        "score": 0,
        "feedback": ""
    }
    
    return app_graph.invoke(initial_state)
