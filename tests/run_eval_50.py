import os
import sys
import random

# Ensure root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.graph import run_resume_batch_workflow

def generate_sample():
    is_resume = random.choice([True, False])
    if is_resume:
        name = random.choice(["Ada Lovelace", "Alan Turing", "Geoffrey Hinton", "Ian Goodfellow", "Yann LeCun", "Andrew Ng", "Fei-Fei Li", "Demis Hassabis", "Yoshua Bengio", "Judea Pearl"])
        skills = random.choice([
            "Python, PyTorch, TensorFlow, LLMs, Transformer Models",
            "Python, Scikit-learn, basic PyTorch, Pandas",
            "Python, HTML, CSS, Javascript"
        ])
        text = f"Resume: {name}\nEmail: {name.lower().replace(' ', '')}@example.com\nSkills: {skills}\nExperience: 5 years in IT."
    else:
        topic = random.choice([
            "Invoice #102 for plumbing\nAcme Corp\nTotal Due: $500",
            "Grandma's recipe for chocolate cake\nIngredients: flour, sugar, cocoa\nBake at 350F",
            "Workout plan: 3 sets of squats\nMonday: Chest\nTuesday: Back",
            "Toyota car manual\nChange oil every 5k miles",
            "Hawaii trip itinerary\nDay 1: Arrive\nDay 2: Beach",
            "Spam offer: click here to win money\nYOU WON $1,000,000!",
            "Grocery list: eggs, milk, flour, bread",
            "Lease Agreement\nTenant: Bob Smith\nRent: $1500/month",
            "Meeting Notes\nQ3 Planning\nDiscussed budget cuts",
            "Roses are red\nViolets are blue\nAI is cool"
        ])
        text = topic
    return text, is_resume

def run_evaluation_50_times():
    print("=====================================================")
    print("      AI RESUME SCREENER - 50x AUTOMATED TESTING     ")
    print("=====================================================")
    
    correct_classifications = 0
    total_runs = 55
    
    jd = "Machine Learning Engineer with Python and PyTorch experience"
    
    for i in range(total_runs):
        text, expected_is_resume = generate_sample()
        # Run workflow
        result = run_resume_batch_workflow(f"test_sample_{i}.pdf", text, jd)
        actual_is_resume = result.get("is_valid_resume")
        
        is_correct = (actual_is_resume == expected_is_resume)
        if is_correct:
            correct_classifications += 1
            
        status = "PASS" if is_correct else "FAIL"
        print(f"Run {i+1:02d}/{total_runs}: Expected Resume={expected_is_resume}, Got={actual_is_resume} -> {status}")
        
    accuracy = (correct_classifications / total_runs) * 100
    print("-----------------------------------------------------")
    print(f"Total Runs: {total_runs}")
    print(f"Correct Classifications: {correct_classifications}")
    print(f"Working Average (Accuracy): {accuracy:.2f}%")
    print("-----------------------------------------------------")
    
    if accuracy >= 98:
        print("RESULT: SUCCESS - Accuracy is above 98%!")
        return True
    else:
        print("RESULT: FAILURE - Accuracy is below 98%!")
        return False

if __name__ == "__main__":
    run_evaluation_50_times()
