from pydantic import BaseModel, Field
from typing import List


class PersonaWouldUseScore(BaseModel):
    persona_id: str
    persona_group: str
    score: float = Field(ge=0, le=10)
    reasoning: str
    supporting_evidence: str


class PersonaGroupScore(BaseModel):
    persona_group: str
    persona_ids: List[str]
    average_score: float = Field(ge=0, le=10)
    reasoning: str
    supporting_evidence: List[str]


class WouldUseResult(BaseModel):
    persona_scores: List[PersonaWouldUseScore]
    group_scores: List[PersonaGroupScore]
    overall_score: float = Field(ge=0, le=10)
    overall_reasoning: str


class WouldUseInput(BaseModel):
    persona_id: str
    persona_group: str
    response: str


class WouldUseRequest(BaseModel):
    product_name: str
    product_description: str
    responses: List[WouldUseInput]


class WouldUseResponse(BaseModel):
    result: WouldUseResult