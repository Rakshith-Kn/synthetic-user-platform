import json
import chromadb

from models.persona import Persona


# -------------------------------------------------
# ChromaDB persistent client
# -------------------------------------------------

client = chromadb.PersistentClient(
    path="./database/chroma"
)


# -------------------------------------------------
# Persona collection
# -------------------------------------------------

persona_collection = client.get_or_create_collection(
    name="personas"
)


# -------------------------------------------------
# Conversation collection
# -------------------------------------------------

conversation_collection = client.get_or_create_collection(
    name="conversations"
)


# =================================================
# PERSONA STORAGE
# =================================================

def store_persona(persona: Persona):

    persona_collection.upsert(
        ids=[persona.persona_id],

        documents=[
            persona.model_dump_json()
        ],

        metadatas=[
            {
                "persona_id": persona.persona_id,
                "name": persona.name
            }
        ]
    )


# =================================================
# GET PERSONA
# =================================================

def get_persona_from_vector_db(
    persona_id: str
):

    result = persona_collection.get(
        ids=[persona_id],
        include=["documents"]
    )

    if not result["documents"]:
        return None

    persona_data = json.loads(
        result["documents"][0]
    )

    return Persona.model_validate(
        persona_data
    )


# =================================================
# STORE CONVERSATION
# =================================================

def store_conversation(
    persona_id: str,
    question: str,
    response: str
):

    conversation_id = (
        f"{persona_id}-"
        f"{len(conversation_collection.get()['ids']) + 1}"
    )

    conversation_collection.add(

        ids=[conversation_id],

        documents=[
            f"Question: {question}\n"
            f"Response: {response}"
        ],

        metadatas=[
            {
                "persona_id": persona_id
            }
        ]
    )


# =================================================
# RETRIEVE RELEVANT CONVERSATIONS
# =================================================

def retrieve_relevant_memory(
    persona_id: str,
    question: str,
    number_of_results: int = 5
):

    result = conversation_collection.query(

        query_texts=[question],

        n_results=number_of_results,

        where={
            "persona_id": persona_id
        }
    )

    if not result["documents"]:
        return []

    return result["documents"][0]