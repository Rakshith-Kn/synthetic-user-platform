from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from models.insight_validation import InsightValidationResult


def validate_insights(
    original_responses: list[str],
    extracted_insights: str
) -> InsightValidationResult:

    # Get Gemini LLM
    llm = get_llm()

    # Force structured validation output
    structured_llm = llm.with_structured_output(
        InsightValidationResult
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an Insight Extraction Validation Agent
for a synthetic user research platform.

Your task is to evaluate whether the extracted
research insights are accurately supported by
the original synthetic user responses.

Evaluate the extracted insights using these
criteria:

1. THEME RELEVANCE
Determine whether the recurring themes are
actually relevant to the original responses.

2. THEME COVERAGE
Determine whether important recurring topics
from the responses were captured.

3. SENTIMENT ACCURACY
Determine whether the sentiment breakdown
accurately represents the responses.

4. AGREEMENT ACCURACY
Determine whether claimed agreement patterns
are actually supported by multiple responses.

5. BEHAVIORAL TREND SUPPORT
Determine whether behavioral trends are
supported by evidence in the responses.

6. PERSONA ATTRIBUTION
Determine whether insights are correctly
connected to the appropriate personas when
persona information is available.

7. REASONING SUPPORT
Determine whether the explanations are
supported by evidence from the original
responses.

SCORING:

0-2:
Very poor or unsupported.

3-4:
Mostly inaccurate or weakly supported.

5-6:
Partially accurate with noticeable gaps.

7-8:
Mostly accurate and well supported.

9-10:
Highly accurate and strongly supported.

IMPORTANT RULES:

- Use ONLY the original responses and
  extracted insights provided.
- Do not invent evidence.
- Do not add information that is absent
  from the responses.
- Do not assume that all personas agree.
- Preserve differences between personas.
- Penalize claims that are not supported.
- Penalize important themes that were omitted.
- Identify contradictions only when they are
  supported by the provided data.
- Be objective and evidence-based.
- Do not make medical claims.

For each criterion, provide a score from 0 to 10.

Also provide:

- Contradictions
- Strengths
- Weaknesses
- Recommendations
- Overall validation score
- Overall reasoning

The overall validation score should reflect
the quality of the extracted insights across
all validation criteria.
"""
        ),
        (
            "human",
            """
ORIGINAL SYNTHETIC USER RESPONSES

{original_responses}


EXTRACTED RESEARCH INSIGHTS

{extracted_insights}


TASK

Validate the extracted research insights against
the original synthetic user responses.

Determine whether the extracted insights are
relevant, complete, accurate, and evidence-based.

Return the structured validation result.
"""
        )
    ])

    chain = prompt | structured_llm

    # Prepare original responses
    responses_text = ""

    for index, response in enumerate(
        original_responses,
        start=1
    ):
        responses_text += (
            f"Response {index}:\n"
            f"{response}\n\n"
        )

    # Run validation
    result = chain.invoke({
        "original_responses": responses_text,
        "extracted_insights": extracted_insights
    })

    return result