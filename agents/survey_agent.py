from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from services.persona_memory import get_persona


def generate_survey_response(
    persona_id: str,
    question: str
):

    # Get the selected persona
    persona = get_persona(persona_id)

    if persona is None:
        raise ValueError(
            f"Persona '{persona_id}' not found."
        )

    # Get Gemini
    llm = get_llm()

    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a synthetic user participating in product research.

Answer the survey question from the perspective
of the given fictional persona.

Maintain consistency with the persona's:

- Personality
- Behavior
- Goals
- Motivations
- Pain points
- Preferences
- Persona group

Do not mention that you are an AI.

Do not mention that you are a synthetic persona.

Answer naturally in first person.

IMPORTANT RESPONSE LENGTH RULES:

- Keep the response SHORT.
- Write only 2 to 4 sentences.
- Aim for approximately 40 to 70 words.
- Answer the question directly.
- Include 1 or 2 important reasons related to the persona.
- Do not repeat the survey question.
- Do not use bullet points or numbered lists.
- Do not give long explanations.
- Do not add unnecessary background information.
- Keep the response realistic and conversational.
"""
        ),
        (
            "human",
            """
PERSONA PROFILE

Name: {name}
Age: {age}
Gender: {gender}
Location: {location}
Occupation: {occupation}
Education: {education}
Persona Group: {persona_group}

PERSONALITY:
{personality}

BEHAVIOR:
{behavior}

PSYCHOLOGY:
{psychology}

SURVEY QUESTION:

{question}

Answer this question as the persona.
Keep the response concise and realistic.
"""
        )
    ])

    chain = prompt | llm

    response = chain.invoke({
        "name": persona.name,
        "age": persona.age,
        "gender": persona.gender,
        "location": persona.location,
        "occupation": persona.occupation,
        "education": persona.education,
        "persona_group": persona.persona_group,
        "personality": persona.personality.model_dump(),
        "behavior": persona.behavior.model_dump(),
        "psychology": persona.psychology.model_dump(),
        "question": question
    })

    # Gemini response
    answer = response.content

    # Handle Gemini content-block response if needed
    if isinstance(answer, list):

        text_parts = []

        for item in answer:

            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

        answer = "".join(text_parts)

    if not isinstance(answer, str):
        answer = str(answer)

    return answer.strip()