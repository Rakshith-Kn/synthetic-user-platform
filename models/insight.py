from pydantic import BaseModel
from typing import List


class InsightRequest(BaseModel):
    responses: List[str]


class InsightResult(BaseModel):
    recurring_themes: List[str]
    sentiment_breakdown: str
    agreement_patterns: List[str]
    behavioral_trends: List[str]
    summary: str


class InsightResponse(BaseModel):
    insights: InsightResult