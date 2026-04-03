import os
from typing import TypedDict
from langchain_core.messages import BaseMessage

try:
    from langchain_openai import ChatOpenAI
    from langchain_anthropic import ChatAnthropic
except ImportError:
    pass

class AgentState(TypedDict):
    file_name: str
    resume_text: str
    job_description: str
    is_valid_resume: bool
    rejection_reason: str
    extracted_profile: dict
    research_results: str
    final_swot: str
    score: int
    feedback: str

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "anthropic":
        return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)
