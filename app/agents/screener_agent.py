from app.schemas.scoring import ExtractedProfile
from app.agents.state import AgentState, get_llm

def screener_node(state: AgentState):
    print(f"[{state['file_name']}] -> Screener Agent: Extracting structured data...")
    text = state['resume_text']
    
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(ExtractedProfile)
        profile = structured_llm.invoke(f"Extract details:\n\n{text}")
        extracted = profile.dict()
    except Exception:
        # Dynamic Mock Fallback
        lines = text.split('\n')
        name = "Unknown"
        email = "N/A"
        skills = []
        for line in lines:
            if line.startswith("Resume:"): name = line.replace("Resume:", "").strip()
            if line.startswith("Email:"): email = line.replace("Email:", "").strip()
            if line.startswith("Skills:"): skills = [s.strip() for s in line.replace("Skills:", "").split(",")]
        
        extracted = {"name": name, "email": email, "skills": skills, "experience_summary": "Parsed dynamically from text."}
    
    return {"extracted_profile": extracted}
