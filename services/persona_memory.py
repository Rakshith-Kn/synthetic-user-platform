from typing import Dict, List, Optional

from models.persona import Persona


from services.vector_memory import (
    store_persona,
    get_persona_from_vector_db,
    store_conversation,
    retrieve_relevant_memory
)



# Stores generated personas
persona_store: Dict[str, Persona] = {}


# Stores conversation history for each persona
conversation_memory: Dict[str, List[dict]] = {}


def store_personas(personas: List[Persona]):

    for persona in personas:

        # Store in temporary memory
        persona_store[persona.persona_id] = persona

        if persona.persona_id not in conversation_memory:
            conversation_memory[persona.persona_id] = []

        # Store persistently in ChromaDB
        store_persona(persona)


def get_persona(
    persona_id: str
) -> Optional[Persona]:

    # First check temporary memory
    persona = persona_store.get(persona_id)

    if persona is not None:
        return persona

    # If not found, retrieve from ChromaDB
    persona = get_persona_from_vector_db(
        persona_id
    )

    if persona is not None:

        # Put it back into temporary memory
        persona_store[persona_id] = persona

    return persona


def get_memory(persona_id: str) -> List[dict]:
    """
    Retrieve previous conversation history.
    """

    return conversation_memory.get(persona_id, [])


def add_memory(
    persona_id: str,
    question: str,
    response: str
):

    if persona_id not in conversation_memory:
        conversation_memory[persona_id] = []

    # Temporary memory
    conversation_memory[persona_id].append({
        "question": question,
        "response": response
    })

    # Persistent memory
    store_conversation(
        persona_id=persona_id,
        question=question,
        response=response
    )