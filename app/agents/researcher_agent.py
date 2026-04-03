from app.agents.state import AgentState

def researcher_node(state: AgentState):
    print(f"[{state['file_name']}] -> Researcher Agent: Simulating web verification...")
    profile = state.get("extracted_profile", {})
    name = profile.get("name", "Unknown")
    
    # Mocking web research
    mock_research = f"Simulated search: Verified {name} has active GitHub repositories matching their skills."
    return {"research_results": mock_research}
