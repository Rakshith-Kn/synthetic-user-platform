from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from services.persona_memory import get_persona
from models.validation import PersonaValidationResult

def validate_persona_consistency(
    persona_id: str,
    responses: list
):

    persona = get_persona(persona_id)

    if persona is None:
        raise ValueError(
            f"Persona '{persona_id}' not found."
        )

    llm = get_llm()
    structured_llm = llm.with_structured_output(
        PersonaValidationResult
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a Persona Consistency Evaluator
for a synthetic user research platform.

Evaluate whether the provided responses remain
consistent with the ACTUAL persona profile.

IMPORTANT:

Use ONLY information explicitly present in the
persona profile and the provided responses.

Do NOT invent:
- occupations
- goals
- motivations
- preferences
- pain points
- personality traits
- previous facts

Evaluate the following parameters:

1. Personality consistency
2. Behavioral consistency
3. Goal consistency
4. Motivation consistency
5. Pain-point consistency
6. Answer-to-answer consistency
7. Response realism

Give each parameter a score from 0 to 10.

10 = highly consistent
5 = partially consistent
0 = highly inconsistent

Identify contradictions only when they are actually
supported by the provided persona profile or responses.

Calculate the overall consistency_score as the
average of the seven parameter scores.

Provide concise evidence-based reasoning.
"""
        ),
        (
            "human",
            """
PERSONA PROFILE

Name: {name}
Age: {age}
Occupation: {occupation}

PERSONALITY:
{personality}

BEHAVIOR:
{behavior}

PSYCHOLOGY:
{psychology}


RESPONSES TO QUESTIONS:

{responses}


Evaluate this persona's consistency.
"""
        )
    ])

    chain = prompt | structured_llm

    response = chain.invoke({
    "name": persona.name,
    "age": persona.age,
    "occupation": persona.occupation,
    "personality": persona.personality.model_dump(),
    "behavior": persona.behavior.model_dump(),
    "psychology": persona.psychology.model_dump(),
    "responses": responses
    })

    return response