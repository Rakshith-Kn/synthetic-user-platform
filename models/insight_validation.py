from pydantic import BaseModel, Field
from typing import List


class InsightValidationResult(BaseModel):

    theme_relevance: float = Field(
        ge=0,
        le=10
    )

    theme_coverage: float = Field(
        ge=0,
        le=10
    )

    sentiment_accuracy: float = Field(
        ge=0,
        le=10
    )

    agreement_accuracy: float = Field(
        ge=0,
        le=10
    )

    behavioral_trend_support: float = Field(
        ge=0,
        le=10
    )

    persona_attribution: float = Field(
        ge=0,
        le=10
    )

    reasoning_support: float = Field(
        ge=0,
        le=10
    )

    contradictions: List[str]

    strengths: List[str]

    weaknesses: List[str]

    recommendations: List[str]

    overall_validation_score: float = Field(
        ge=0,
        le=10
    )

    overall_reasoning: str


class InsightValidationRequest(BaseModel):

    original_responses: List[str]

    extracted_insights: str


class InsightValidationResponse(BaseModel):

    validation: InsightValidationResult