
from services.report_generator import build_research_report


def test_pdf_report_is_generated():
    data = {
        "project_title": "Test Research Report",
        "product_name": "CareSphere AI",
        "product_description": "Healthcare and wellness platform",
        "research_objective": "Test product usefulness",
        "scenario_name": "Test Scenario",
        "persona_profiles": [
            {
                "persona_id": "CS-001",
                "name": "Test Persona",
                "occupation": "Teacher",
            }
        ],
        "survey_responses": [
            {
                "persona_id": "CS-001",
                "persona_name": "Test Persona",
                "response": "I value privacy and simple features.",
            }
        ],
        "interview_responses": [],
        "insight_summary": {
            "recurring_themes": ["Privacy"],
            "sentiment_breakdown": "Cautiously positive",
            "agreement_patterns": ["Users value privacy"],
            "behavioral_trends": ["Prefer clear controls"],
            "summary": "Privacy may influence adoption.",
        },
        "would_use_result": {
            "overall_score": 7,
            "overall_reasoning": "Useful features",
            "persona_scores": [],
            "group_scores": [],
        },
        "consistency_results": [],
        "insight_validation": {
            "overall_validation_score": 8,
            "overall_reasoning": "Themes are supported",
        },
    }

    pdf = build_research_report(data)

    assert isinstance(pdf, bytes)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 500


def test_pdf_handles_empty_research_sections():
    data = {
        "project_title": "Empty Research Report",
        "product_name": "Test Product",
    }

    pdf = build_research_report(data)

    assert pdf.startswith(b"%PDF")
