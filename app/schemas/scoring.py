from pydantic import BaseModel, Field
from typing import List

class ClassificationResult(BaseModel):
    is_valid_resume: bool = Field(description="True if the text appears to be a resume, False if it is junk/invoice/recipe etc.")
    reason: str = Field(description="Explanation of why it is or isn't a resume.")

class ExtractedProfile(BaseModel):
    name: str = Field(description="The name of the applicant")
    email: str = Field(description="The email of the applicant")
    skills: List[str] = Field(description="List of all skills mentioned")
    experience_summary: str = Field(description="A brief summary of past work experience")

class AnalystScore(BaseModel):
    score: int = Field(description="A score from 0 to 100 on how well the candidate matches the ML job description")
    swot_analysis: str = Field(description="Strengths, Weaknesses, Opportunities, Threats analysis")
