import os
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn

from app.services.utils import extract_text_from_pdf
from app.agents.graph import run_resume_batch_workflow
from app.services.integration import add_resume_to_notion

load_dotenv()

app = FastAPI(title="AI Resume Screener API")

MOCK_JD = """
Machine Learning Engineer with Deep Learning and PyTorch. 3+ years experience.
"""

@app.get("/")
def read_root():
    return {"status": "AI Resume Screener is running..."}

@app.post("/webhook/resume")
async def receive_resume(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "File must be a PDF."})
    
    os.makedirs("temp_resumes", exist_ok=True)
    file_path = f"temp_resumes/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    background_tasks.add_task(process_resume_workflow, file_path, file.filename)
    
    return {"status": "processing", "message": f"Resume {file.filename} queued for analysis."}

def process_resume_workflow(file_path: str, file_name: str):
    print(f"[{file_name}] Starting Multi-Agent workflow...")
    
    resume_text = extract_text_from_pdf(file_path)
    if not resume_text or resume_text == "Could not parse PDF text.":
        print(f"[{file_name}] Failed to extract text.")
        return
        
    final_state = run_resume_batch_workflow(file_name, resume_text, MOCK_JD)
    
    if final_state.get("is_valid_resume"):
        profile = final_state.get("extracted_profile", {})
        research = final_state.get("research_results", "")
        score = final_state.get("score", 0)
        swot = final_state.get("final_swot", "")
        
        add_resume_to_notion(profile, research, score, swot)
    
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Could not remove temp file {file_path}: {e}")
        
    print(f"[{file_name}] Workflow Complete!")

if __name__ == "__main__":
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
