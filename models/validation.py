from pydantic import BaseModel, Field
from typing import List


class PersonaValidationRequest(BaseModel):
    persona_id: str
    responses: List[str]


class PersonaValidationResult(BaseModel):
    personality_consistency: float = Field(ge=0, le=10)
    behavior_consistency: float = Field(ge=0, le=10)
    goal_consistency: float = Field(ge=0, le=10)
    motivation_consistency: float = Field(ge=0, le=10)
    pain_point_consistency: float = Field(ge=0, le=10)
    answer_consistency: float = Field(ge=0, le=10)
    response_realism: float = Field(ge=0, le=10)

    contradictions: List[str]

    reasoning: str

    consistency_score: float = Field(
        ge=0,
        le=10
    )


class PersonaValidationResponse(BaseModel):
    persona_id: str
    validation: PersonaValidationResult