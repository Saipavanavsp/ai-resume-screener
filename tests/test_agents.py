import pytest
from app.schemas.scoring import ExtractedProfile, AnalystScore, ClassificationResult

def test_classification_result_schema():
    data = {"is_valid_resume": True, "reason": "Contains experience sections."}
    obj = ClassificationResult(**data)
    assert obj.is_valid_resume is True
    assert "experience" in obj.reason

def test_extracted_profile_schema():
    data = {
        "name": "Alan Turing",
        "email": "alan@turing.com",
        "skills": ["Math", "Cryptography", "Computing"],
        "experience_summary": "Cracked enigma, invented computing."
    }
    obj = ExtractedProfile(**data)
    assert len(obj.skills) == 3
    assert obj.name == "Alan Turing"

def test_analyst_score_validation():
    with pytest.raises(Exception):
        # Missing required field
        AnalystScore(score=85)
    
    valid_obj = AnalystScore(score=85, swot_analysis="Strengths: math. Weakness: none.")
    assert valid_obj.score == 85
