from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from models.persona import PersonaGenerationResponse


def generate_personas(
    product_name: str,
    product_description: str,
    target_audience: str,
    research_objective: str,
    number_of_personas: int
):

    # ---------------------------------------------------------
    # Get Gemini
    # ---------------------------------------------------------

    llm = get_llm()

    # Force Gemini to follow the Pydantic schema
    structured_llm = llm.with_structured_output(
        PersonaGenerationResponse
    )

    # ---------------------------------------------------------
    # Persona Generation Prompt
    # ---------------------------------------------------------

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert Synthetic User Persona Generation Agent
for product research.

Your job is to create realistic, fictional and diverse
research participants who genuinely represent the specified
target audience.

The personas will later participate in:

- Survey experiments
- Interview experiments
- Persona consistency validation
- Insight extraction
- Would-Use scoring

Therefore, each persona must represent a meaningful
research segment and must produce noticeably different
but realistic opinions.

============================================================
CORE REQUIREMENTS
============================================================

1. Generate exactly the requested number of personas.

2. Every persona must belong to the specified target audience.

3. Every persona must be fictional.

4. Every persona must have a UNIQUE persona_id.

5. Every persona must have a UNIQUE full name within
   this generation.

6. Do NOT repeatedly use common names such as the same
   names from previous examples.

7. Use varied realistic first names and surnames.

8. Do not create famous people or real identifiable people.

============================================================
PERSONA DIVERSITY
============================================================

Create meaningful diversity across:

- Age
- Gender
- Location
- Occupation
- Education
- Technology adoption
- Digital literacy
- Price sensitivity
- Decision style
- Buying behavior
- Goals
- Motivations
- Pain points
- Preferences
- Trust level
- Privacy concerns
- Healthcare involvement
- Convenience needs

The personas should NOT feel like variations of the
same person.

============================================================
OCCUPATION DIVERSITY
============================================================

Occupation is especially important.

Do NOT generate mostly:

- Software engineers
- Software architects
- Developers
- Computer scientists
- IT professionals
- Psychologists
- Researchers

unless the target audience explicitly requires them.

For a general healthcare and wellness product, consider
realistic occupations from DIFFERENT fields, for example:

- Teacher
- Accountant
- Business owner
- Healthcare administrator
- Nurse
- Consultant
- Marketing professional
- Government employee
- Sales professional
- Designer
- Engineer
- Entrepreneur
- Service professional
- Homemaker
- Student
- Retired professional

These are examples only.

Do NOT force these exact occupations.

Choose occupations that naturally fit the generated
persona's age, education, lifestyle and behavior.

The occupation must NOT determine the persona's entire
personality.

============================================================
IMPORTANT HEALTHCARE PRODUCT RULE
============================================================

If the product is healthcare or wellness related,
DO NOT assume that every user is a healthcare professional.

The product's target users may come from many professions.

For example, an accountant, teacher, business owner,
engineer, administrator or retired person can all be
users of a healthcare management platform.

Healthcare experience should be represented through:

- Healthcare usage
- Wellness habits
- Family healthcare responsibilities
- Digital health experience
- Privacy expectations
- Trust
- Convenience
- Insurance concerns
- Medication management expectations
- Appointment management
- Technology comfort

It should NOT automatically be represented by making
the person's occupation a healthcare occupation.

============================================================
EDUCATION DIVERSITY
============================================================

Do not give every persona a master's degree.

Education should vary realistically, for example:

- High school
- Diploma
- Bachelor's degree
- Master's degree
- Professional qualification
- Doctorate
- Other appropriate education

Education must logically fit the occupation.

============================================================
PERSONA GROUP
============================================================

Every persona MUST have a meaningful persona_group.

The persona_group must represent a behavioral,
psychological or research-relevant segment.

Do NOT create groups based only on:

- Age
- Gender
- Location
- Occupation

Examples:

- Technology-First Efficiency Seekers
- Privacy-Conscious Skeptics
- Wellness-Focused Convenience Seekers
- Budget-Conscious Value Maximizers
- Family Healthcare Managers
- Trust-Focused Users
- Convenience-Oriented Users
- Cautious Digital Health Users
- Independence-Focused Users
- Early Digital Health Adopters

These are examples only.

Create groups appropriate to the actual
persona characteristics.

============================================================
INTERNAL CONSISTENCY
============================================================

Each persona must be internally consistent.

For example:

A privacy-conscious persona should show privacy
concerns in personality, behavior and psychology.

A budget-conscious persona should show price sensitivity
and value-oriented decision making.

A technology-first persona may value integrations
and automation.

A convenience-focused persona may prioritize simplicity
and reduced effort.

Do not create contradictions between the persona's
occupation, personality, behavior and psychology.

============================================================
HEALTHCARE SAFETY
============================================================

Do not invent serious medical diagnoses or medical
conditions unless explicitly required by the research
scenario.

Focus on:

- User needs
- Preferences
- Behaviors
- Trust
- Privacy
- Accessibility
- Convenience
- Digital literacy
- Expectations
- Healthcare management habits

============================================================
RESEARCH VALUE
============================================================

Each persona must have a distinct perspective that can
produce meaningful differences during:

Survey Mode
Interview Mode
Insight Extraction
Would-Use scoring

Do not make every persona enthusiastic about AI.

Do not make every persona highly technical.

Do not make every persona highly educated.

Do not make every persona price-sensitive.

Do not make every persona privacy-focused.

Create realistic variation.

============================================================
FINAL CHECK BEFORE RETURNING
============================================================

Before returning the structured output, internally verify:

- Correct number of personas
- Unique persona IDs
- Unique names
- Diverse occupations
- Diverse education levels
- Diverse ages
- Diverse behavioral groups
- Different technology adoption levels
- Different price sensitivities
- Different motivations
- Different pain points
- Internal consistency
- All personas belong to the target audience

Return only the structured output required by the schema.
"""
        ),
        (
            "human",
            """
============================================================
PRODUCT INFORMATION
============================================================

Product Name:
{product_name}

Product Description:
{product_description}

Target Audience:
{target_audience}

Research Objective:
{research_objective}

Number of Personas:
{number_of_personas}

============================================================
TASK
============================================================

Generate exactly {number_of_personas} fictional synthetic
user personas for this research experiment.

IMPORTANT:

The personas must represent REALISTIC USERS of the
target audience.

Do not make the personas employees, developers or
experts of the product unless the target audience
specifically requires that.

For a healthcare and wellness platform, create users
from different professions and life situations who
would realistically manage healthcare or wellness
using digital tools.

Make the personas sufficiently different so that when
they answer the same survey question, their responses
reflect different motivations, concerns and priorities.

Every persona must have:

- Unique persona ID
- Unique full name
- Diverse occupation
- Appropriate education
- Meaningful persona group
- Distinct personality
- Distinct behavior
- Distinct psychological characteristics
- Consistent goals
- Consistent motivations
- Consistent pain points
- Consistent preferences

Do not make the occupations mostly technology-related.

Do not make all personas highly educated.

Do not make all personas healthcare professionals.

Do not make all personas interested in AI.

Return only the structured persona generation output.
"""
        )
    ])

    # ---------------------------------------------------------
    # Generate Personas
    # ---------------------------------------------------------

    chain = prompt | structured_llm

    result = chain.invoke({
        "product_name": product_name,
        "product_description": product_description,
        "target_audience": target_audience,
        "research_objective": research_objective,
        "number_of_personas": number_of_personas
    })

    # ---------------------------------------------------------
    # PROGRAMMATIC VALIDATION
    # ---------------------------------------------------------

    personas = result.personas

    # Check number
    if len(personas) != number_of_personas:
        raise ValueError(
            f"Expected {number_of_personas} personas, "
            f"but generated {len(personas)}."
        )

    # Check duplicate persona IDs
    persona_ids = [
        persona.persona_id.strip().lower()
        for persona in personas
    ]

    if len(persona_ids) != len(set(persona_ids)):
        raise ValueError(
            "Duplicate persona IDs detected. "
            "Please generate the personas again."
        )

    # Check duplicate names
    names = [
        persona.name.strip().lower()
        for persona in personas
    ]

    if len(names) != len(set(names)):
        raise ValueError(
            "Duplicate persona names detected. "
            "Please generate the personas again."
        )

    # ---------------------------------------------------------
    # Occupation Diversity Check
    # ---------------------------------------------------------

    occupations = [
        persona.occupation.strip().lower()
        for persona in personas
    ]

    unique_occupations = set(occupations)

    # For 4+ personas, require at least 3 different occupations.
    # For 3 personas, require at least 2.
    # For 1-2 personas, every occupation must still be unique.
    if number_of_personas >= 4:
        minimum_occupations = 3
    elif number_of_personas == 3:
        minimum_occupations = 2
    else:
        minimum_occupations = number_of_personas

    if len(unique_occupations) < minimum_occupations:
        raise ValueError(
            "Insufficient occupation diversity detected. "
            "Please generate the personas again."
        )

    # ---------------------------------------------------------
    # Technology Occupation Check
    # ---------------------------------------------------------

    technology_terms = {
        "software",
        "developer",
        "programmer",
        "computer scientist",
        "software architect",
        "it professional",
        "data scientist",
        "devops",
        "technology consultant"
    }

    technology_count = 0

    for occupation in occupations:

        if any(
            term in occupation
            for term in technology_terms
        ):
            technology_count += 1

    # Do not allow the majority of personas to have
    # technology-focused occupations.
    if number_of_personas >= 4:

        if technology_count > number_of_personas / 2:

            raise ValueError(
                "Too many technology-related occupations "
                "were generated. Please generate a more "
                "diverse research participant set."
            )

    # ---------------------------------------------------------
    # Return Validated Result
    # ---------------------------------------------------------

    return result