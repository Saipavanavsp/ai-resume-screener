from app.schemas.scoring import AnalystScore
from app.agents.state import AgentState, get_llm

def analyst_node(state: AgentState):
    print(f"[{state['file_name']}] -> Analyst Agent: Comparing to Job Description & Scoring...")
    text = state['resume_text'].lower()
    profile = state.get("extracted_profile", {})
    
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(AnalystScore)
        prompt = f"Candidate Profile:\n{profile}\n\nJob Description:\n{state['job_description']}\n\nScore?"
        result = structured_llm.invoke(prompt)
        score = result.score
        swot = result.swot_analysis
    except Exception:
        # Dynamic Mock Fallback Scoring!
        if "pytorch" in text or "tensorflow" in text:
            score = 95
            swot = "Strengths: Expert deep learning skills. Weakness: None identified."
        elif "scikit-learn" in text:
            score = 75
            swot = "Strengths: Solid machine learning basics. Weakness: Lacks deep LLM/Transformer experience."
        else:
            score = 45
            swot = "Strengths: Basic coding. Weakness: Lacks advanced AI/ML skills required for role."
            
    return {"score": score, "final_swot": swot}
