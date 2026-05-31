class HeuristicClassifier:
    def __init__(self):
        self.resume_keywords = ["experience", "education", "skills", "projects", "employment", "work history", "summary", "qualification"]
        self.junk_keywords = ["invoice", "recipe", "ingredients", "bake", "lease", "tenant", "rent", "workout", "gym", "shopping list", "spam", "won $", "winner"]
        
    def classify(self, text: str) -> dict:
        text_lower = text.lower()
        
        # Check junk keywords first
        for keyword in self.junk_keywords:
            if keyword in text_lower:
                return {
                    "is_valid_resume": False,
                    "reason": f"Heuristic: Contains junk keyword '{keyword}'."
                }
                
        # Check resume keywords
        matches = [kw for kw in self.resume_keywords if kw in text_lower]
        if len(matches) >= 2 or "skills:" in text_lower or "experience:" in text_lower:
            return {
                "is_valid_resume": True,
                "reason": f"Heuristic: Found resume keywords: {', '.join(matches)}."
            }
            
        return {
            "is_valid_resume": False,
            "reason": "Heuristic: Lacks standard resume section keywords."
        }
