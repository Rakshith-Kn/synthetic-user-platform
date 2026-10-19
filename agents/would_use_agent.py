from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from models.would_use import WouldUseResult


def calculate_would_use_score(
    product_name: str,
    product_description: str,
    responses: list
) -> WouldUseResult:

    # Get Gemini LLM
    llm = get_llm()

    # Force Gemini to return the required structured output
    structured_llm = llm.with_structured_output(
        WouldUseResult
    )

    # Prompt for the Would-Use scoring agent
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a Would-Use Product Evaluation Agent
for a synthetic user research platform.

Your task is to analyze synthetic user research
responses and determine how likely each persona
would be to use the given product.

For EVERY persona:

1. Identify the persona_id.
2. Identify the persona_group.
3. Give a score from 0 to 10.
4. Explain the reasoning behind the score.
5. Provide supporting evidence from the actual response.

Then group personas according to their
persona_group.

For EVERY persona group:

1. List all persona IDs belonging to the group.
2. Calculate the average score of the personas
   in that group.
3. Explain the reasoning behind the group score.
4. Provide supporting evidence from the responses.

Finally:

1. Calculate the overall score across all personas.
2. Explain the overall result.

IMPORTANT RULES:

- Use ONLY the provided research responses.
- Do not invent persona opinions.
- Do not invent supporting evidence.
- Preserve differences between personas.
- Do not assume every persona wants the product.
- Do not use demographic information alone to
  determine the score.
- Consider explicit interest, usefulness,
  trust, concerns, adoption barriers and
  willingness to use the product.
- Scores must be between 0 and 10.
- Keep reasoning evidence-based.
- Do not make medical claims.
- Do not change persona IDs.
- Do not change persona groups.

SCORING GUIDANCE:

0-2:
Very unlikely to use the product.

3-4:
Unlikely to use the product unless major concerns
are addressed.

5-6:
Moderately interested but has significant
concerns or conditions.

7-8:
Likely to use the product with relatively
minor concerns.

9-10:
Very likely to use the product and expresses
strong interest or clear value.

The score must be based on the actual response
provided by each persona.
"""
        ),
        (
            "human",
            """
PRODUCT INFORMATION

Product Name:
{product_name}

Product Description:
{product_description}


SYNTHETIC USER RESEARCH RESPONSES

{responses}


TASK

Evaluate how likely each synthetic persona is to
use this product.

Generate:

1. Individual persona scores.
2. Persona-group scores.
3. Overall score.
4. Evidence-based reasoning for all scores.

Make sure every persona from the input is represented
in the output.

Keep the analysis strictly grounded in the
provided research responses.
"""
        )
    ])

    # Connect prompt to Gemini
    chain = prompt | structured_llm

    # Prepare persona responses for Gemini
    responses_text = ""

    for index, item in enumerate(responses, start=1):

        responses_text += (
            f"Response {index}\n"
            f"Persona ID: {item.persona_id}\n"
            f"Persona Group: {item.persona_group}\n"
            f"Response: {item.response}\n\n"
        )

    # Generate structured result
    result = chain.invoke({
        "product_name": product_name,
        "product_description": product_description,
        "responses": responses_text
    })

    return result