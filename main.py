from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI
from fastapi.responses import Response

# ============================================================
# MODELS
# ============================================================
from models.survey import SurveyRequest, SurveyResponse, SurveyResponseItem
from models.validation import PersonaValidationRequest, PersonaValidationResponse
from models.insight import InsightRequest, InsightResponse
from models.insight_validation import InsightValidationRequest, InsightValidationResponse
from models.would_use import WouldUseRequest, WouldUseResponse
from models.persona import PersonaGenerationRequest
from models.survey_scenario import SurveyScenario
from models.research_report import ResearchReportRequest

# ============================================================
# AGENTS
# ============================================================
from agents.consistency_agent import validate_persona_consistency
from agents.insight_agent import extract_insights
from agents.insight_validation_agent import validate_insights
from agents.would_use_agent import calculate_would_use_score
from agents.survey_agent import generate_survey_response
from agents.persona_agent import generate_personas
from agents.interview_agent import interview_persona

# ============================================================
# SERVICES
# ============================================================
from services.persona_memory import get_persona, store_personas
from services.report_generator import build_research_report

# ============================================================
# FASTAPI APPLICATION
# ============================================================
app = FastAPI(
    title="Synthetic User Research Platform",
    description="Backend API for AI-powered synthetic user generation",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Synthetic User Research Backend is running!"}

@app.post("/personas")
def create_personas(request: PersonaGenerationRequest):
    result = generate_personas(
        product_name=request.product_name,
        product_description=request.product_description,
        target_audience=request.target_audience,
        research_objective=request.research_objective,
        number_of_personas=request.number_of_personas
    )
    store_personas(result.personas)
    return result

@app.post("/personas/{persona_id}/interview")
def interview(persona_id: str, question: str):
    response = interview_persona(persona_id=persona_id, question=question)
    return {"persona_id": persona_id, "question": question, "response": response}

def generate_single_survey_response(persona_id: str, question: str):
    persona = get_persona(persona_id)
    if persona is None:
        raise ValueError(f"Persona '{persona_id}' not found.")
    answer = generate_survey_response(persona_id=persona_id, question=question)
    return SurveyResponseItem(
        persona_id=persona_id,
        persona_name=persona.name,
        response=answer
    )

@app.post("/survey", response_model=SurveyResponse)
def run_survey(request: SurveyRequest):
    with ThreadPoolExecutor(max_workers=max(1, len(request.persona_ids))) as executor:
        responses = list(executor.map(
            lambda persona_id: generate_single_survey_response(
                persona_id=persona_id,
                question=request.question
            ),
            request.persona_ids
        ))
    return SurveyResponse(question=request.question, responses=responses)

@app.post("/survey-scenario", response_model=SurveyResponse)
def run_survey_scenario(scenario: SurveyScenario):
    with ThreadPoolExecutor(max_workers=max(1, len(scenario.persona_ids))) as executor:
        responses = list(executor.map(
            lambda persona_id: generate_single_survey_response(
                persona_id=persona_id,
                question=scenario.question
            ),
            scenario.persona_ids
        ))
    return SurveyResponse(question=scenario.question, responses=responses)

@app.post("/validate-consistency", response_model=PersonaValidationResponse)
def validate_consistency(request: PersonaValidationRequest):
    evaluation = validate_persona_consistency(
        persona_id=request.persona_id,
        responses=request.responses
    )
    return PersonaValidationResponse(persona_id=request.persona_id, validation=evaluation)

@app.post("/insights", response_model=InsightResponse)
def generate_insights(request: InsightRequest):
    insights = extract_insights(request.responses)
    return InsightResponse(insights=insights)

@app.post("/would-use-score", response_model=WouldUseResponse)
def generate_would_use_score(request: WouldUseRequest):
    result = calculate_would_use_score(
        product_name=request.product_name,
        product_description=request.product_description,
        responses=request.responses
    )
    return WouldUseResponse(result=result)

@app.post("/validate-insights", response_model=InsightValidationResponse)
def validate_extracted_insights(request: InsightValidationRequest):
    validation = validate_insights(
        original_responses=request.original_responses,
        extracted_insights=request.extracted_insights
    )
    return InsightValidationResponse(validation=validation)

@app.post("/research-report")
def generate_research_report(request: ResearchReportRequest):
    """Create a downloadable PDF from supplied synthetic-user research results."""
    report_data = request.model_dump()
    pdf_bytes = build_research_report(report_data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="synthetic_user_research_report.pdf"'}
    )
