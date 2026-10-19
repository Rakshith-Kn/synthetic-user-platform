from pydantic import BaseModel, Field
from typing import List


class Personality(BaseModel):
    openness: float = Field(ge=0, le=1)
    conscientiousness: float = Field(ge=0, le=1)
    extraversion: float = Field(ge=0, le=1)
    agreeableness: float = Field(ge=0, le=1)
    neuroticism: float = Field(ge=0, le=1)


class Behavior(BaseModel):
    technology_adoption: str
    price_sensitivity: str
    decision_style: str
    buying_behavior: str


class PsychologicalProfile(BaseModel):
    goals: List[str]
    motivations: List[str]
    pain_points: List[str]
    preferences: List[str]


class Persona(BaseModel):
    persona_id: str
    name: str
    age: int
    gender: str
    location: str
    occupation: str
    education: str
    persona_group: str

    personality: Personality
    behavior: Behavior
    psychology: PsychologicalProfile


class PersonaGenerationRequest(BaseModel):
    product_name: str
    product_description: str
    target_audience: str
    research_objective: str
    number_of_personas: int = Field(
        default=5,
        ge=1,
        le=100
    )


class PersonaGenerationResponse(BaseModel):
    personas: List[Persona]