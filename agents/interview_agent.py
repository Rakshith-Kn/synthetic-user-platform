from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from services.persona_memory import (
    get_persona,
    get_memory,
    add_memory
)


def interview_persona(
    persona_id: str,
    question: str
):
    """
    Generate a response from a synthetic persona
    while considering its profile and previous
    conversation history.
    """

    # -------------------------------------------------
    # 1. Retrieve the persona
    # -------------------------------------------------

    persona = get_persona(persona_id)

    if persona is None:
        raise ValueError(
            f"Persona '{persona_id}' not found."
        )

    # -------------------------------------------------
    # 2. Retrieve previous conversation memory
    # -------------------------------------------------

    previous_memory = get_memory(persona_id)

    # Convert memory into readable text
    memory_text = ""

    for item in previous_memory:
        memory_text += (
            f"Question: {item['question']}\n"
            f"Response: {item['response']}\n\n"
        )

    if not memory_text:
        memory_text = "No previous conversation."

    # -------------------------------------------------
    # 3. Get Gemini LLM
    # -------------------------------------------------

    llm = get_llm()

    # -------------------------------------------------
    # 4. Create interview prompt
    # -------------------------------------------------

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a Synthetic User Interview Agent.

Your job is to answer questions as the specified
fictional synthetic user.

IMPORTANT RULES:

1. Stay consistent with the persona's:
   - Demographic information
   - Personality
   - Behavior
   - Goals
   - Motivations
   - Pain points
   - Preferences

2. Use previous conversation history when answering.

3. Do not contradict previous answers unless the
   current question provides a valid reason for
   changing an opinion.

4. Answer naturally from the persona's perspective.

5. Use first-person language such as:
   "I", "me", "my", and "I would".

6. Do not mention that you are an AI.

7. Do not mention that you are a synthetic persona.

8. Do not describe the persona from an outside
   perspective.

9. Give realistic product-research responses.

10. Keep the response relevant to the question.
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

PERSONALITY

{personality}

BEHAVIOR

{behavior}

PSYCHOLOGICAL PROFILE

{psychology}


PREVIOUS CONVERSATION

{memory}


CURRENT QUESTION

{question}


Respond to the current question as this persona.

Use the persona's profile and previous conversation
to maintain consistency.
"""
        )
    ])

    # -------------------------------------------------
    # 5. Create LangChain chain
    # -------------------------------------------------

    chain = prompt | llm

    # -------------------------------------------------
    # 6. Generate response
    # -------------------------------------------------

    response = chain.invoke({
        "name": persona.name,
        "age": persona.age,
        "gender": persona.gender,
        "location": persona.location,
        "occupation": persona.occupation,
        "education": persona.education,
        "personality": persona.personality.model_dump(),
        "behavior": persona.behavior.model_dump(),
        "psychology": persona.psychology.model_dump(),
        "memory": memory_text,
        "question": question
    })

    # -------------------------------------------------
    # 7. Extract answer from Gemini response
    # -------------------------------------------------

    answer = response.content

    # Gemini may return content as a list of blocks
    if isinstance(answer, list):

        text_parts = []

        for item in answer:

            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(
                        item.get("text", "")
                    )

        answer = "".join(text_parts)

    # Make sure the final answer is always a string
    if not isinstance(answer, str):
        answer = str(answer)

    # -------------------------------------------------
    # 8. Save the new interaction to memory
    # -------------------------------------------------

    add_memory(
        persona_id=persona_id,
        question=question,
        response=answer
    )

    # -------------------------------------------------
    # 9. Return the answer
    # -------------------------------------------------

    return answer