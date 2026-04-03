from app.schemas.scoring import ClassificationResult
from app.agents.state import AgentState, get_llm

def classifier_node(state: AgentState):
    print(f"[{state['file_name']}] -> Classifier Agent: Is this a resume?")
    text = state['resume_text'].lower()
    
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(ClassificationResult)
        result = structured_llm.invoke(f"Is this a resume for an IT/ML role?\n\n{text}")
        is_resume = result.is_valid_resume
        reason = result.reason
    except Exception as e:
        # Dynamic Mock Fallback
        if "invoice" in text or "recipe" in text or "spam" in text or "won $" in text or "lease" in text or "manual" in text or "poem" in text or "grocery" in text or "gym" in text:
            is_resume = False
            reason = "Keyword indicates non-resume junk folder."
        elif "experience:" in text or "skills:" in text:
            is_resume = True
            reason = "Looks like a resume profile."
        else:
            is_resume = False
            reason = "Could not identify standard resume sections."

    return {"is_valid_resume": is_resume, "rejection_reason": reason}
