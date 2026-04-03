import os
import sys

# Ensure the root directory is accessible for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.utils import extract_text_from_pdf
from app.agents.graph import run_resume_batch_workflow

MOCK_JD = """
Machine Learning Engineer
Required Skills: Python, Deep Learning, PyTorch, TensorFlow.
Experience: 3+ years building ML models and training transformers.
"""

def process_batch():
    directory = "batch_pdfs"
    # Go up one level to find the folder from the root since script moved
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(root_dir, directory)
    
    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} not found! Run generate_batch.py first.")
        return

    print("=====================================================")
    print("      AI RESUME SCREENER - BULK PROCESSING           ")
    print("=====================================================")
    
    files = os.listdir(target_dir)
    print(f"Total incoming files found: {len(files)}")
    
    valid_candidates = []
    rejected_files = []

    for filename in files:
        file_path = os.path.join(target_dir, filename)
        
        text = extract_text_from_pdf(file_path)
        if not text or text == "Could not parse PDF text.":
            rejected_files.append((filename, "Failed to read PDF"))
            continue
            
        results = run_resume_batch_workflow(filename, text, MOCK_JD)
        
        if not results.get("is_valid_resume"):
            rejected_files.append((filename, results.get("rejection_reason", "Junk/Spam")))
        else:
            profile = results.get("extracted_profile", {})
            valid_candidates.append({
                "file": filename,
                "name": profile.get("name", "Unknown"),
                "score": results.get("score", 0),
                "swot": results.get("final_swot", "No SWOT generated")
            })

    valid_candidates.sort(key=lambda x: x["score"], reverse=True)

    print("\n-----------------------------------------------------")
    print(f"                 FILTER REPORT                      ")
    print("-----------------------------------------------------")
    print(f"Total Invalid/Junk files rejected: {len(rejected_files)}")
    for j in rejected_files:
        print(f" [X] {j[0]} -> {j[1]}")

    print("\n=====================================================")
    print("             ML CANDIDATE LEADERBOARD                ")
    print("=====================================================")
    if not valid_candidates:
        print("No valid resumes found.")
    else:
        for i, c in enumerate(valid_candidates, 1):
            star = "[EXPERT]" if c['score'] >= 90 else ("[INTERMEDIATE]" if c['score'] >= 70 else "[JUNIOR]")
            print(f"#{i} | Score: {c['score']} {star} | Name: {c['name']}")
            print(f"    File: {c['file']}")
            print(f"    SWOT: {c['swot']}\n")

if __name__ == "__main__":
    process_batch()
