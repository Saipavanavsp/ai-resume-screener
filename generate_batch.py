import os
from reportlab.pdfgen import canvas
import random

def create_pdf(filename, lines):
    c = canvas.Canvas(filename)
    y = 750
    for line in lines:
        c.drawString(50, y, line)
        y -= 20
    c.save()

def generate_resumes():
    os.makedirs("batch_pdfs", exist_ok=True)
    
    # Generate 10 ML Resumes with varying quality
    ml_names = ["Ada Lovelace", "Alan Turing", "Geoffrey Hinton", "Ian Goodfellow", 
                "Yann LeCun", "Andrew Ng", "Fei-Fei Li", "Demis Hassabis", 
                "Yoshua Bengio", "Judea Pearl"]
    
    for i, name in enumerate(ml_names):
        quality = random.choice(["Expert", "Intermediate", "Beginner"])
        if quality == "Expert":
            skills = "Python, PyTorch, TensorFlow, LLMs, Transformer Models, MLOps"
            exp = "8 years as Lead AI Engineer. Built 5 production LLM systems."
            points = "Has PhD in CS. Built state of the art models."
        elif quality == "Intermediate":
            skills = "Python, Scikit-learn, basic PyTorch, Pandas"
            exp = "3 years as Data Scientist. Built some predictive models."
            points = "Familiar with basic ML concepts. Learning deep learning."
        else:
            skills = "Python, HTML, CSS, Javascript"
            exp = "1 year junior software developer."
            points = "Read an article about AI once."
            
        lines = [
            f"Resume: {name}",
            f"Email: {name.split()[0].lower()}@example.com",
            f"Skills: {skills}",
            f"Experience: {exp}",
            f"Details: {points}"
        ]
        create_pdf(f"batch_pdfs/resume_ml_{i}.pdf", lines)

    # Generate 10 Random Junk files (Invoices, Spam, Recipes)
    junk_topics = [
        ("Invoice 001", ["Invoice #001", "To: Acme Corp", "Total: $500", "For: Plumbing services"]),
        ("Chocolate Cake Recipe", ["Grandma's Cake", "Ingredients: Flour, Sugar, Cocoa", "Bake at 350F"]),
        ("Car Manual", ["Toyota Camry 2005 Manual", "Change oil every 5k miles", "Tire pressure 32 PSI"]),
        ("Vacation Itinerary", ["Hawaii Trip", "Day 1: Arrive", "Day 2: Beach", "Day 3: Volcano tour"]),
        ("Spam Offer", ["YOU WON $1,000,000!", "Click here to claim your prize!", "No credit card needed!"]),
        ("Grocery List", ["Milk", "Eggs", "Bread", "Coffee", "Bananas"]),
        ("Meeting Notes", ["Q3 Planning", "Discussed budget cuts", "Alice to handle marketing"]),
        ("Poem", ["Roses are red", "Violets are blue", "AI is cool", "And so are you"]),
        ("Gym Workout", ["Monday: Chest", "Tuesday: Back", "Wednesday: Legs", "Friday: Rest"]),
        ("Apartment Lease", ["Lease Agreement", "Tenant: Bob Smith", "Rent: $1500/month", "No pets allowed"])
    ]
    
    for i, (title, lines) in enumerate(junk_topics):
        create_pdf(f"batch_pdfs/junk_{i}.pdf", lines)

    print("Generated 20 PDFs successfully in 'batch_pdfs/' directory!")

if __name__ == "__main__":
    generate_resumes()
