from pydantic import BaseModel
from typing import List


class SurveyRequest(BaseModel):
    question: str
    persona_ids: List[str]


class SurveyResponseItem(BaseModel):
    persona_id: str
    persona_name: str
    response: str


class SurveyResponse(BaseModel):
    question: str
    responses: List[SurveyResponseItem]
    
class SurveyScenario(BaseModel):
    scenario_name: str
    product_name: str
    product_description: str
    research_objective: str
    question: str