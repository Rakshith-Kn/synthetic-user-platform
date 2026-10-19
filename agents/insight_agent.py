from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from models.insight import InsightResult


def extract_insights(responses: list[str]) -> InsightResult:

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        InsightResult
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an Insight Extraction Agent for a
synthetic user research platform.

Analyze the provided synthetic user research
responses and extract evidence-based insights.

Identify:

1. Recurring Themes
   - Identify topics mentioned repeatedly.
   - Do not invent themes that are not supported
     by the responses.

2. Sentiment Breakdown
   - Identify the overall sentiment across responses.
   - Mention positive, negative, and neutral patterns
     where applicable.

3. Agreement Patterns
   - Identify areas where multiple personas agree.
   - Also identify important disagreements between
     personas.

4. Behavioral Trends
   - Identify common behavioral patterns.
   - Explain what the responses suggest about
     user behavior.

5. Summary
   - Provide a concise overall research summary.

IMPORTANT:

- Use ONLY the provided responses.
- Do not invent information.
- Do not assume that all personas think alike.
- Preserve differences between personas.
- Base insights on patterns appearing across
  the responses.
- Do not make medical claims.
"""
        ),
        (
            "human",
            """
RESEARCH RESPONSES

{responses}

Analyze these responses and extract structured
research insights.
"""
        )
    ])

    chain = prompt | structured_llm

    responses_text = ""

    for index, response in enumerate(responses, start=1):
        responses_text += (
            f"Persona Response {index}:\n"
            f"{response}\n\n"
        )

    result = chain.invoke({
        "responses": responses_text
    })

    return result