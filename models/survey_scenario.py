from pydantic import BaseModel, Field
from typing import List


class SurveyScenario(BaseModel):
    scenario_name: str

    product_name: str

    product_description: str

    target_audience: str

    research_objective: str

    question: str

    persona_ids: List[str] = Field(
        min_length=1
    )