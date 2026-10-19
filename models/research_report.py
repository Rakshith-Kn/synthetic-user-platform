
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ResearchReportRequest(BaseModel):
    project_title: str = "Synthetic User Research Report"
    product_name: str
    product_description: str = ""
    research_objective: str = ""
    scenario_name: str = "Research Experiment"

    persona_profiles: List[Dict[str, Any]] = Field(default_factory=list)
    survey_responses: List[Dict[str, Any]] = Field(default_factory=list)
    interview_responses: List[Dict[str, Any]] = Field(default_factory=list)

    insight_summary: Dict[str, Any] = Field(default_factory=dict)
    would_use_result: Dict[str, Any] = Field(default_factory=dict)
    consistency_results: List[Dict[str, Any]] = Field(default_factory=list)
    insight_validation: Dict[str, Any] = Field(default_factory=dict)
