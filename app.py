import pandas as pd
import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Synthetic Lab",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "personas" not in st.session_state:
    st.session_state.personas = []

if "survey_results" not in st.session_state:
    st.session_state.survey_results = []

if "survey_history" not in st.session_state:
    st.session_state.survey_history = {}

if "interview_messages" not in st.session_state:
    st.session_state.interview_messages = {}

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = None

if "insights" not in st.session_state:
    st.session_state.insights = None

if "consistency_result" not in st.session_state:
    st.session_state.consistency_result = None

if "would_use_result" not in st.session_state:
    st.session_state.would_use_result = None

if "insight_validation" not in st.session_state:
    st.session_state.insight_validation = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ---------- GENERAL ---------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stApp {
    background-color: #080c14;
    color: #f8fafc;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background-color: #0d121d;
    border-right: 1px solid #20283a;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}


/* ---------- HEADINGS ---------- */

h1, h2, h3, h4 {
    color: #f8fafc !important;
}

p, span, label {
    color: #aeb8ca;
}


/* ---------- HERO ---------- */

.hero {
    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(116, 96, 255, 0.25),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #111827,
            #12172a
        );

    border: 1px solid #293248;
    border-radius: 24px;
    padding: 38px;
    margin-bottom: 28px;
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 16px;
    color: #9ca8bd;
    margin-top: 10px;
    max-width: 800px;
}

.live-badge {
    display: inline-block;
    margin-top: 20px;
    padding: 6px 13px;
    border-radius: 20px;
    background: rgba(46, 204, 113, 0.10);
    border: 1px solid rgba(46, 204, 113, 0.25);
    color: #55e6a5;
    font-size: 12px;
}


/* ---------- CARDS ---------- */

.card {
    background: #101622;
    border: 1px solid #222c3f;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.card-title {
    color: #ffffff;
    font-size: 19px;
    font-weight: 700;
}

.card-subtitle {
    color: #8d99ad;
    font-size: 13px;
    margin-top: 5px;
}


/* ---------- METRICS ---------- */

.metric-card {
    background: #101622;
    border: 1px solid #222c3f;
    border-radius: 17px;
    padding: 20px;
}

.metric-number {
    color: #ffffff;
    font-size: 30px;
    font-weight: 800;
}

.metric-label {
    color: #8490a5;
    font-size: 13px;
    margin-top: 5px;
}


/* ---------- PERSONA ---------- */

.persona-card {
    background: #101622;
    border: 1px solid #242e42;
    border-radius: 19px;
    padding: 23px;
    min-height: 245px;
    margin-bottom: 18px;
}

.persona-name {
    font-size: 21px;
    font-weight: 750;
    color: #ffffff;
}

.persona-group {
    color: #9b8cff;
    font-size: 13px;
    margin-top: 5px;
    margin-bottom: 17px;
}

.persona-info {
    color: #a1adbf;
    font-size: 13px;
    line-height: 1.8;
}


/* ---------- RESPONSE ---------- */

.response-card {
    background: #0f1521;
    border: 1px solid #283247;
    border-radius: 17px;
    padding: 22px;
    min-height: 230px;
}

.response-name {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
}

.response-group {
    color: #9b8cff;
    font-size: 12px;
    margin-top: 3px;
    margin-bottom: 17px;
}

.response-text {
    color: #c4ccda;
    font-size: 14px;
    line-height: 1.75;
}


/* ---------- CHAT ---------- */

.chat-user {
    background: #1b2232;
    border-radius: 15px;
    padding: 15px 18px;
    margin: 10px 0;
    color: #e5eaf2;
}

.chat-persona {
    background: #111a2b;
    border: 1px solid #26334b;
    border-radius: 15px;
    padding: 15px 18px;
    margin: 10px 0;
    color: #c9d1df;
}


/* ---------- SCORE ---------- */

.score {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
}

.score-label {
    color: #8995aa;
    font-size: 13px;
}


/* ---------- BUTTONS ---------- */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #303b51;
    background: #151c2a;
    color: #ffffff;
    font-weight: 650;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #60a5fa;
    background: #1c2436;
}


/* ---------- INPUTS ---------- */

textarea,
input {
    color: #ffffff !important;
}


/* ---------- DIVIDER ---------- */

hr {
    border-color: #202a3d !important;
}



/* ---------- GLASSMORPHISM / BLUE ACCENT ---------- */
:root {
    --sl-blue: #3b82f6;
    --sl-blue-bright: #93c5fd;
    --sl-glass: rgba(15, 25, 43, 0.62);
    --sl-glass-border: rgba(147, 197, 253, 0.22);
}

.stApp {
    background:
        radial-gradient(ellipse at 8% 0%, rgba(37, 99, 235, 0.24), transparent 36%),
        radial-gradient(ellipse at 92% 10%, rgba(14, 165, 233, 0.14), transparent 32%),
        linear-gradient(135deg, #060b14 0%, #0a1222 52%, #07101d 100%);
    background-attachment: fixed;
}

.block-container { max-width: 1480px; padding-top: 1.5rem; padding-bottom: 3.5rem; }
h1, h2, h3, h4 { letter-spacing: -0.025em; }
h2, h3 { margin-top: 0.35rem; }

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(19, 39, 68, 0.76), rgba(10, 20, 36, 0.58));
    border: 1px solid rgba(147, 197, 253, 0.28);
    border-radius: 24px;
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255,255,255,0.07);
}
.hero:after { color: rgba(191, 219, 254, 0.18); }

.card, .metric-card, .persona-card, .response-card,
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(22, 37, 59, 0.68), rgba(10, 20, 35, 0.60));
    border: 1px solid rgba(147, 197, 253, 0.17);
    border-radius: 18px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 12px 34px rgba(0,0,0,0.16), inset 0 1px 0 rgba(255,255,255,0.035);
    transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}
.card:hover, .metric-card:hover, .persona-card:hover, .response-card:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-2px);
    border-color: rgba(147, 197, 253, 0.42);
    box-shadow: 0 16px 38px rgba(0,0,0,0.22), 0 0 24px rgba(37,99,235,0.08);
}
.metric-number, .score {
    background: linear-gradient(100deg, #ffffff 5%, #93c5fd 85%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.persona-group, .response-group {
    display: inline-block; color: #bfdbfe;
    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(147, 197, 253, 0.22);
    border-radius: 999px; padding: 4px 10px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(12, 25, 44, 0.92), rgba(7, 14, 26, 0.94));
    border-right: 1px solid rgba(147, 197, 253, 0.18);
    backdrop-filter: blur(22px);
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }
section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: #91a7c4; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em;
}
section[data-testid="stSidebar"] [role="radiogroup"] { gap: 6px; }
section[data-testid="stSidebar"] [role="radiogroup"] > label {
    background: rgba(255,255,255,0.025); border: 1px solid transparent;
    border-radius: 13px; padding: 9px 12px;
    transition: background 160ms ease, border-color 160ms ease;
}
section[data-testid="stSidebar"] [role="radiogroup"] > label:hover {
    background: rgba(59,130,246,0.10); border-color: rgba(147,197,253,0.24);
}
section[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, rgba(37,99,235,0.28), rgba(59,130,246,0.07));
    border-color: rgba(147,197,253,0.38);
}

.stButton > button, .stDownloadButton > button {
    border-radius: 13px; border: 1px solid rgba(147,197,253,0.34);
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: #fff; font-weight: 700; min-height: 44px;
    box-shadow: 0 8px 22px rgba(29,78,216,0.22);
    transition: transform 160ms ease, filter 160ms ease, box-shadow 160ms ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: #bfdbfe; background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: #fff; transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(29,78,216,0.30);
}
.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div,
.stNumberInput input, .stDateInput input {
    background: rgba(7, 16, 30, 0.72) !important;
    border-color: rgba(147,197,253,0.22) !important;
    border-radius: 12px !important;
}
[data-testid="stMetric"] { padding: 16px 18px; }
[data-testid="stMetricLabel"] p { color: #9bb0ca !important; }
[data-testid="stMetricValue"] { color: #eff6ff !important; }

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.025); border-radius: 10px 10px 0 0;
    padding: 10px 15px;
}
.stTabs [aria-selected="true"] { border-bottom-color: #60a5fa !important; color: #bfdbfe !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid rgba(147,197,253,0.16); border-radius: 14px; overflow: hidden;
}
hr { border-color: rgba(147,197,253,0.14) !important; }

@media (max-width: 768px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1rem; }
    .hero { border-radius: 18px; }
    h1 { font-size: 1.9rem !important; }
}
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# API HELPERS
# ============================================================

def backend_online():
    try:
        response = requests.get(
            f"{API_URL}/",
            timeout=5
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def generate_personas_api(
    product_name,
    product_description,
    target_audience,
    research_objective,
    number_of_personas
):
    response = requests.post(
        f"{API_URL}/personas",
        json={
            "product_name": product_name,
            "product_description": product_description,
            "target_audience": target_audience,
            "research_objective": research_objective,
            "number_of_personas": number_of_personas
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()


def run_survey_api(scenario):
    response = requests.post(
        f"{API_URL}/survey-scenario",
        json=scenario,
        timeout=180
    )

    response.raise_for_status()

    return response.json()


def run_interview_api(persona_id, question):
    response = requests.post(
        f"{API_URL}/personas/{persona_id}/interview",
        params={
            "question": question
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()


def run_consistency_api(persona_id, responses):
    response = requests.post(
        f"{API_URL}/validate-consistency",
        json={
            "persona_id": persona_id,
            "responses": responses
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()


def run_insights_api(responses):
    response = requests.post(
        f"{API_URL}/insights",
        json={
            "responses": responses
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()


def run_would_use_api(product_name, product_description, responses):
    response = requests.post(
        f"{API_URL}/would-use-score",
        json={
            "product_name": product_name,
            "product_description": product_description,
            "responses": responses
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()


def run_insight_validation_api(
    original_responses,
    extracted_insights
):
    response = requests.post(
        f"{API_URL}/validate-insights",
        json={
            "original_responses": original_responses,
            "extracted_insights": extracted_insights
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# BACKEND STATUS
# ============================================================

is_online = backend_online()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:24px;
            font-weight:800;
            color:white;
        ">
            ✦ Synthetic Lab
        </div>

        <div style="
            color:#7f8ba1;
            font-size:12px;
            margin-top:4px;
            margin-bottom:25px;
        ">
            AI Product Research Studio
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "WORKSPACE",
        [
            "Overview",
            "Personas",
            "Survey Mode",
            "Interview Mode",
            "Insights & Analysis",
            "Research Dashboard"
        ]
    )

    st.divider()

    if is_online:
        st.success("Backend Connected")
    else:
        st.error("Backend Offline")

    st.caption("CareSphere AI")
    st.caption("Synthetic User Research")


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Synthetic User Research
            </div>

            <div class="hero-subtitle">
                Simulate diverse product users, conduct structured
                research experiments, and transform synthetic
                responses into actionable research insights.
            </div>

            <div class="live-badge">
                ● Research Workspace
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Research Overview")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("04", "Synthetic Personas"),
        ("03", "Survey Scenarios"),
        ("02", "Research Modes"),
        ("05", "AI Agents")
    ]

    for column, (number, label) in zip(
        [c1, c2, c3, c4],
        metrics
    ):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{number}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("## Current Product")

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        CareSphere AI
        </div>

        <div class="card-subtitle">
        AI-powered healthcare and wellness management platform
        for appointments, health tracking, medication reminders,
        AI assistance and insurance management.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Research Pipeline")

    c1, c2, c3, c4 = st.columns(4)

    pipeline = [
        ("01", "Personas", "Generate diverse synthetic users."),
        ("02", "Research", "Run surveys and interviews."),
        ("03", "Insights", "Extract research patterns."),
        ("04", "Validation", "Validate findings and consistency.")
    ]

    for column, (num, title, text) in zip(
        [c1, c2, c3, c4],
        pipeline
    ):
        with column:
            st.markdown(
                f"""
                <div class="card">

                <div style="
                    color:#8f81ff;
                    font-size:12px;
                    font-weight:700;
                ">
                {num}
                </div>

                <div class="card-title">
                {title}
                </div>

                <div class="card-subtitle">
                {text}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# PERSONAS
# ============================================================

elif page == "Personas":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Synthetic Personas
            </div>

            <div class="hero-subtitle">
                Generate realistic research participants with
                demographic, behavioral and psychological profiles.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if not is_online:
        st.error(
            "FastAPI is not running. Start it with: "
            "uvicorn main:app --reload"
        )
        st.stop()

    c1, c2 = st.columns([1.5, 1])

    with c1:

        product_name = st.text_input(
            "Product Name",
            value="CareSphere AI"
        )

        product_description = st.text_area(
            "Product Description",
            value=(
                "An AI-powered healthcare and wellness management "
                "platform providing appointment management, health "
                "tracking, medication reminders, AI health assistance "
                "and insurance management."
            ),
            height=120
        )

    with c2:

        target_audience = st.text_area(
            "Target Audience",
            value=(
                "Adults who regularly manage healthcare and "
                "wellness activities using digital platforms."
            ),
            height=120
        )

        number_of_personas = st.number_input(
            "Number of Personas",
            min_value=1,
            max_value=10,
            value=4
        )

    research_objective = st.text_area(
        "Research Objective",
        value=(
            "Understand how different user segments perceive "
            "the usefulness, trustworthiness and usability of "
            "an integrated AI healthcare and wellness platform."
        )
    )

    if st.button(
        "✦ Generate Synthetic Personas",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Persona Generation Agent is creating research participants..."
        ):

            try:

                result = generate_personas_api(
                    product_name,
                    product_description,
                    target_audience,
                    research_objective,
                    number_of_personas
                )

                st.session_state.personas = result["personas"]

                st.success(
                    f"{len(st.session_state.personas)} personas generated successfully."
                )

            except Exception as error:

                st.error(
                    f"Persona generation failed: {error}"
                )

    if st.session_state.personas:

        st.divider()

        st.markdown("## Research Participants")

        personas = st.session_state.personas

        for start in range(0, len(personas), 2):

            columns = st.columns(2)

            for i, column in enumerate(columns):

                index = start + i

                if index >= len(personas):
                    continue

                persona = personas[index]

                with column:

                    st.markdown(
                        f"""
                        <div class="persona-card">

                        <div style="font-size:25px;">
                        👤
                        </div>

                        <div class="persona-name">
                        {persona["name"]}
                        </div>

                        <div class="persona-group">
                        {persona.get(
                            "persona_group",
                            "Synthetic Research Participant"
                        )}
                        </div>

                        <div class="persona-info">

                        <b>Age:</b> {persona["age"]}
                        <br>

                        <b>Location:</b> {persona["location"]}
                        <br>

                        <b>Occupation:</b> {persona["occupation"]}
                        <br>

                        <b>Education:</b> {persona["education"]}

                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# ============================================================
# SURVEY MODE
# ============================================================

elif page == "Survey Mode":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Survey Mode
            </div>

            <div class="hero-subtitle">
                Ask the same research question to multiple
                synthetic users and compare their perspectives.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.personas:

        st.warning(
            "No personas available. Go to Personas and generate them first."
        )
        st.stop()

    scenario = st.selectbox(
        "Research Scenario",
        [
            "Trust & Privacy Evaluation",
            "Usability Evaluation",
            "Pricing & Value Evaluation",
            "Custom Research Question"
        ]
    )

    questions = {
        "Trust & Privacy Evaluation":
            "What would make CareSphere AI trustworthy or untrustworthy for managing your healthcare information?",

        "Usability Evaluation":
            "Which features would make CareSphere AI easy or difficult for you to use regularly?",

        "Pricing & Value Evaluation":
            "What would make CareSphere AI worth paying for, and what pricing or cost-related factors would prevent you from subscribing?"
    }

    if scenario == "Custom Research Question":

        question = st.text_area(
            "Research Question",
            height=110
        )

    else:

        question = st.text_area(
            "Research Question",
            value=questions[scenario],
            height=110
        )

    selected_ids = []

    st.markdown("### Select Personas")

    columns = st.columns(4)

    for index, persona in enumerate(
        st.session_state.personas
    ):

        with columns[index % 4]:

            selected = st.checkbox(
                persona["name"],
                value=True,
                key=f"survey_persona_{persona['persona_id']}"
            )

            if selected:
                selected_ids.append(
                    persona["persona_id"]
                )

    if st.button(
        "✦ Run Survey",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():
            st.error("Please enter a research question.")

        elif not selected_ids:
            st.error("Select at least one persona.")

        else:

            payload = {
                "scenario_name": scenario,
                "product_name": "CareSphere AI",
                "product_description": (
                    "An AI-powered healthcare and wellness "
                    "management platform providing appointment "
                    "management, health tracking, medication "
                    "reminders, AI health assistance and "
                    "insurance management."
                ),
                "target_audience": (
                    "Adults who regularly manage healthcare "
                    "and wellness activities using digital platforms."
                ),
                "research_objective": (
                    "Understand how different user segments "
                    "perceive CareSphere AI."
                ),
                "question": question,
                "persona_ids": selected_ids
            }

            with st.spinner(
                "Survey Agent is interviewing the selected personas..."
            ):

                try:

                    result = run_survey_api(payload)

                    st.session_state.survey_results = result["responses"]

                    # Store responses for consistency validation.
                    for item in result["responses"]:

                        persona_id = item["persona_id"]

                        if persona_id not in st.session_state.survey_history:
                            st.session_state.survey_history[persona_id] = []

                        st.session_state.survey_history[
                            persona_id
                        ].append(item["response"])

                    st.success(
                        "Survey completed successfully."
                    )

                except Exception as error:

                    st.error(
                        f"Survey failed: {error}"
                    )

    # Display results

    if st.session_state.survey_results:

        st.divider()

        st.markdown("## Survey Responses")

        responses = st.session_state.survey_results

        for start in range(0, len(responses), 2):

            columns = st.columns(2)

            for i, column in enumerate(columns):

                index = start + i

                if index >= len(responses):
                    continue

                item = responses[index]

                persona = next(
                    (
                        p for p in st.session_state.personas
                        if p["persona_id"] == item["persona_id"]
                    ),
                    None
                )

                group = ""

                if persona:
                    group = persona.get(
                        "persona_group",
                        ""
                    )

                with column:

                    st.markdown(
                        f"""
                        <div class="response-card">

                        <div class="response-name">
                        {item["persona_name"]}
                        </div>

                        <div class="response-group">
                        {group}
                        </div>

                        <div class="response-text">
                        {item["response"]}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# ============================================================
# INTERVIEW MODE
# ============================================================

elif page == "Interview Mode":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Interview Mode
            </div>

            <div class="hero-subtitle">
                Conduct a continuous conversation with a selected
                synthetic persona while preserving context through
                persistent memory.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.personas:

        st.warning(
            "Generate personas first."
        )
        st.stop()

    persona_names = {
        p["name"]: p
        for p in st.session_state.personas
    }

    selected_name = st.selectbox(
        "Select Persona",
        list(persona_names.keys())
    )

    persona = persona_names[selected_name]

    st.markdown(
        f"""
        <div class="card">

        <div class="card-title">
        👤 {persona["name"]}
        </div>

        <div class="card-subtitle">
        {persona.get("persona_group", "")}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    persona_id = persona["persona_id"]

    if persona_id not in st.session_state.interview_messages:
        st.session_state.interview_messages[persona_id] = []

    for message in st.session_state.interview_messages[persona_id]:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="chat-user">
                <b>You</b><br>
                {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="chat-persona">
                <b>{persona["name"]}</b><br>
                {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    question = st.text_input(
        "Ask the persona",
        placeholder="Ask something about CareSphere AI..."
    )

    if st.button(
        "Send Interview Question",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():

            st.error(
                "Please enter a question."
            )

        else:

            with st.spinner(
                f"{persona['name']} is responding..."
            ):

                try:

                    result = run_interview_api(
                        persona_id,
                        question
                    )

                    answer = result["response"]

                    st.session_state.interview_messages[
                        persona_id
                    ].append(
                        {
                            "role": "user",
                            "content": question
                        }
                    )

                    st.session_state.interview_messages[
                        persona_id
                    ].append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Interview failed: {error}"
                    )


# ============================================================
# INSIGHTS & ANALYSIS
# ============================================================

elif page == "Insights & Analysis":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Insights & Analysis
            </div>

            <div class="hero-subtitle">
                Transform collected research responses into
                structured insights, scores and validation results.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.survey_results:

        st.warning(
            "Run a Survey first so the analysis agents have responses to analyze."
        )
        st.stop()

    responses = [
        item["response"]
        for item in st.session_state.survey_results
    ]

    st.markdown("## Research Analysis")

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "✦ Extract Insights",
            use_container_width=True
        ):

            with st.spinner(
                "Insight Extraction Agent is analyzing responses..."
            ):

                try:

                    result = run_insights_api(
                        responses
                    )

                    st.session_state.insights = result["insights"]

                    st.success(
                        "Insights generated."
                    )

                except Exception as error:

                    st.error(
                        f"Insight extraction failed: {error}"
                    )

    with c2:

        if st.button(
            "◈ Validate Consistency",
            use_container_width=True
        ):

            persona = st.session_state.personas[0]

            persona_id = persona["persona_id"]

            persona_responses = st.session_state.survey_history.get(
                persona_id,
                []
            )

            if len(persona_responses) < 2:

                st.warning(
                    "Run at least two different survey scenarios "
                    "for the same persona before validating consistency."
                )

            else:

                with st.spinner(
                    "Consistency Agent is validating the persona..."
                ):

                    try:

                        result = run_consistency_api(
                            persona_id,
                            persona_responses
                        )

                        st.session_state.consistency_result = result

                    except Exception as error:

                        st.error(
                            f"Consistency validation failed: {error}"
                        )

    with c3:

        if st.button(
            "◎ Would-Use Analysis",
            use_container_width=True
        ):

            would_use_inputs = []

            for item in st.session_state.survey_results:

                persona = next(
                    (
                        p for p in st.session_state.personas
                        if p["persona_id"] == item["persona_id"]
                    ),
                    None
                )

                if persona:

                    would_use_inputs.append(
                        {
                            "persona_id": persona["persona_id"],
                            "persona_group": persona.get(
                                "persona_group",
                                "Unknown"
                            ),
                            "response": item["response"]
                        }
                    )

            with st.spinner(
                "Would-Use Agent is calculating scores..."
            ):

                try:

                    result = run_would_use_api(
                        "CareSphere AI",
                        (
                            "An AI-powered healthcare and wellness "
                            "management platform providing appointment "
                            "management, health tracking, medication "
                            "reminders, AI health assistance and "
                            "insurance management."
                        ),
                        would_use_inputs
                    )

                    st.session_state.would_use_result = result

                except Exception as error:

                    st.error(
                        f"Would-use analysis failed: {error}"
                    )

    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    if st.session_state.insights:

        st.divider()

        st.markdown("## Extracted Insights")

        insights = st.session_state.insights

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### Recurring Themes")

            for theme in insights.get(
                "recurring_themes",
                []
            ):

                st.markdown(
                    f"• {theme}"
                )

        with c2:

            st.markdown("### Agreement Patterns")

            for pattern in insights.get(
                "agreement_patterns",
                []
            ):

                st.markdown(
                    f"• {pattern}"
                )

        st.markdown("### Sentiment")

        st.info(
            insights.get(
                "sentiment_breakdown",
                ""
            )
        )

        st.markdown("### Behavioral Trends")

        for trend in insights.get(
            "behavioral_trends",
            []
        ):

            st.markdown(
                f"• {trend}"
            )

        st.markdown("### Summary")

        st.write(
            insights.get(
                "summary",
                ""
            )
        )

    # --------------------------------------------------------
    # WOULD USE
    # --------------------------------------------------------

    if st.session_state.would_use_result:

        st.divider()

        st.markdown("## Would-Use Analysis")

        result = st.session_state.would_use_result[
            "result"
        ]

        c1, c2 = st.columns([1, 2])

        with c1:

            st.markdown(
                f"""
                <div class="card">

                <div class="score">
                {result["overall_score"]}/10
                </div>

                <div class="score-label">
                Overall Would-Use Score
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown("### Overall Reasoning")

            st.write(
                result["overall_reasoning"]
            )

        st.markdown("### Persona Scores")

        for item in result["persona_scores"]:

            c1, c2, c3 = st.columns([1.5, 1, 4])

            with c1:
                st.write(
                    f"**{item['persona_id']}**"
                )

            with c2:
                st.write(
                    f"**{item['score']}/10**"
                )

            with c3:
                st.write(
                    item["reasoning"]
                )

    # --------------------------------------------------------
    # CONSISTENCY
    # --------------------------------------------------------

    if st.session_state.consistency_result:

        st.divider()

        st.markdown("## Persona Consistency")

        validation = st.session_state.consistency_result[
            "validation"
        ]

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Overall Consistency",
                f"{validation['consistency_score']}/10"
            )

        with c2:

            st.metric(
                "Response Realism",
                f"{validation['response_realism']}/10"
            )

        with c3:

            st.metric(
                "Answer Consistency",
                f"{validation['answer_consistency']}/10"
            )

        if validation["contradictions"]:

            st.warning("Contradictions detected:")

            for item in validation["contradictions"]:
                st.write(
                    f"• {item}"
                )

        else:

            st.success(
                "No contradictions detected."
            )

        st.write(
            validation["reasoning"]
        )

    # --------------------------------------------------------
    # INSIGHT VALIDATION
    # --------------------------------------------------------

    if st.session_state.insights:

        st.divider()

        if st.button(
            "✓ Validate Extracted Insights",
            use_container_width=True
        ):

            extracted = str(
                st.session_state.insights
            )

            with st.spinner(
                "Insight Validation Agent is checking the findings..."
            ):

                try:

                    result = run_insight_validation_api(
                        responses,
                        extracted
                    )

                    st.session_state.insight_validation = result

                except Exception as error:

                    st.error(
                        f"Insight validation failed: {error}"
                    )

    if st.session_state.insight_validation:

        validation = st.session_state.insight_validation[
            "validation"
        ]

        st.markdown("## Insight Validation")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Overall Validation",
                f"{validation['overall_validation_score']}/10"
            )

        with c2:

            st.metric(
                "Theme Relevance",
                f"{validation['theme_relevance']}/10"
            )

        with c3:

            st.metric(
                "Sentiment Accuracy",
                f"{validation['sentiment_accuracy']}/10"
            )

        st.markdown("### Strengths")

        for item in validation["strengths"]:
            st.write(
                f"• {item}"
            )

        st.markdown("### Weaknesses")

        for item in validation["weaknesses"]:
            st.write(
                f"• {item}"
            )

        st.markdown("### Recommendations")

        for item in validation["recommendations"]:
            st.write(
                f"• {item}"
            )

        st.markdown("### Validation Reasoning")

        st.write(
            validation["overall_reasoning"]
        )

# ============================================================
# RESEARCH DASHBOARD AND PDF REPORT
# ============================================================

elif page == "Research Dashboard":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Research Dashboard</div>
            <div class="hero-subtitle">
                Visualize your experiment findings and generate a downloadable PDF report.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    personas = st.session_state.personas or []
    survey_results = st.session_state.survey_results or []
    insights = st.session_state.insights or {}
    would_use_data = st.session_state.would_use_result or {}
    consistency_data = st.session_state.consistency_result or {}
    insight_validation_data = st.session_state.insight_validation or {}

    # Normalize API response wrappers used by this project.
    would_use = would_use_data.get("result", would_use_data) if isinstance(would_use_data, dict) else {}
    consistency = consistency_data.get("validation", consistency_data) if isinstance(consistency_data, dict) else {}
    insight_validation = insight_validation_data.get("validation", insight_validation_data) if isinstance(insight_validation_data, dict) else {}

    # Turn interview chat messages into reportable question/answer pairs.
    interview_results = []
    for persona in personas:
        persona_id = persona.get("persona_id", "")
        messages = st.session_state.interview_messages.get(persona_id, [])
        for index in range(0, len(messages) - 1, 2):
            user_message = messages[index]
            assistant_message = messages[index + 1]
            if user_message.get("role") == "user" and assistant_message.get("role") == "assistant":
                interview_results.append({
                    "persona_id": persona_id,
                    "persona_name": persona.get("name", "Persona"),
                    "question": user_message.get("content", ""),
                    "response": assistant_message.get("content", "")
                })

    st.subheader("Experiment Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Personas", len(personas))
    c2.metric("Survey Responses", len(survey_results))
    c3.metric("Interview Turns", len(interview_results))
    overall_score = would_use.get("overall_score") if isinstance(would_use, dict) else None
    c4.metric(
        "Would-Use Score",
        f"{overall_score}/10" if isinstance(overall_score, (int, float)) else "Not calculated"
    )

    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("Recurring Themes")
        themes = insights.get("recurring_themes", []) if isinstance(insights, dict) else []
        if themes:
            for index, theme in enumerate(themes, start=1):
                st.markdown(f"**{index}. {theme}**")
        else:
            st.info("Run Extract Insights in Insights & Analysis to populate themes.")

    with right:
        st.subheader("Sentiment Breakdown")
        if insights:
            st.write(insights.get("sentiment_breakdown", "Sentiment not available."))
        else:
            st.info("No insight results available yet.")

    st.subheader("Agreement Patterns")
    patterns = insights.get("agreement_patterns", []) if isinstance(insights, dict) else []
    if patterns:
        for pattern in patterns:
            st.write(f"• {pattern}")
    else:
        st.caption("No agreement patterns available.")

    st.subheader("Behavioral Trends")
    trends = insights.get("behavioral_trends", []) if isinstance(insights, dict) else []
    if trends:
        for trend in trends:
            st.write(f"• {trend}")
    else:
        st.caption("No behavioral trends available.")

    st.divider()
    st.subheader("Key Persona Quotes")
    if survey_results:
        for item in survey_results[:12]:
            with st.container(border=True):
                st.markdown(f"**{item.get('persona_name', item.get('persona_id', 'Persona'))}**")
                st.write(item.get("response", ""))
    else:
        st.info("Run a survey to display persona quotes.")

    if interview_results:
        st.markdown("### Interview Highlights")
        for item in interview_results[:8]:
            with st.container(border=True):
                st.markdown(f"**{item['persona_name']}**")
                st.caption(f"Question: {item['question']}")
                st.write(item["response"])

    st.divider()
    st.subheader("Product Adoption Scores")
    persona_scores = would_use.get("persona_scores", []) if isinstance(would_use, dict) else []
    if persona_scores:
        score_rows = [
            {
                "Persona": item.get("persona_id", "Unknown"),
                "Group": item.get("persona_group", "Unknown"),
                "Score": item.get("score", 0)
            }
            for item in persona_scores
        ]
        score_frame = pd.DataFrame(score_rows)
        st.bar_chart(score_frame.set_index("Persona")["Score"])
        st.dataframe(score_frame, use_container_width=True, hide_index=True)
    else:
        st.info("Run Would-Use Analysis in Insights & Analysis to display scores.")

    group_scores = would_use.get("group_scores", []) if isinstance(would_use, dict) else []
    if group_scores:
        st.markdown("### Persona Group Scores")
        group_frame = pd.DataFrame([
            {
                "Persona Group": item.get("persona_group", "Unknown"),
                "Average Score": item.get("average_score", 0)
            }
            for item in group_scores
        ])
        st.bar_chart(group_frame.set_index("Persona Group")["Average Score"])
        st.dataframe(group_frame, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Validation Results")
    validation_columns = st.columns(2)
    with validation_columns[0]:
        if consistency:
            st.metric("Persona Consistency", f"{consistency.get('consistency_score', 'N/A')}/10")
            st.write(consistency.get("reasoning", ""))
            contradictions = consistency.get("contradictions", [])
            if contradictions:
                st.warning("Contradictions detected")
                for item in contradictions:
                    st.write(f"• {item}")
        else:
            st.caption("Persona consistency results are not available yet.")

    with validation_columns[1]:
        if insight_validation:
            st.metric(
                "Insight Validation",
                f"{insight_validation.get('overall_validation_score', 'N/A')}/10"
            )
            st.write(insight_validation.get("overall_reasoning", ""))
            for heading, key in [("Strengths", "strengths"), ("Weaknesses", "weaknesses"), ("Recommendations", "recommendations")]:
                values = insight_validation.get(key, [])
                if values:
                    st.markdown(f"**{heading}**")
                    for value in values:
                        st.write(f"• {value}")
        else:
            st.caption("Insight validation results are not available yet.")

    st.divider()
    st.subheader("Download Research Report")
    report_product_name = st.text_input("Product name", "CareSphere AI", key="report_product_name")
    report_product_description = st.text_area(
        "Product description",
        "AI-powered healthcare and wellness platform for appointments, health tracking, medication reminders, AI assistance and insurance management.",
        key="report_product_description"
    )
    report_scenario_name = st.text_input(
        "Experiment scenario", "CareSphere AI Research Experiment", key="report_scenario_name"
    )
    report_objective = st.text_area(
        "Research objective",
        "Evaluate user trust, usability, product usefulness and willingness to use CareSphere AI.",
        key="report_research_objective"
    )

    if st.button("Generate PDF Report", type="primary", use_container_width=True):
        report_payload = {
            "project_title": "Synthetic User Research Report",
            "product_name": report_product_name,
            "product_description": report_product_description,
            "research_objective": report_objective,
            "scenario_name": report_scenario_name,
            "persona_profiles": personas,
            "survey_responses": survey_results,
            "interview_responses": interview_results,
            "insight_summary": insights,
            "would_use_result": would_use,
            "consistency_results": [consistency] if consistency else [],
            "insight_validation": insight_validation
        }
        try:
            with st.spinner("Generating your PDF report..."):
                response = requests.post(
                    f"{API_URL}/research-report",
                    json=report_payload,
                    timeout=120
                )
            if response.status_code == 200 and "application/pdf" in response.headers.get("content-type", ""):
                st.download_button(
                    "Download PDF Report",
                    data=response.content,
                    file_name="synthetic_user_research_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("Your PDF report is ready.")
            else:
                st.error(
                    f"Report generation failed ({response.status_code}): {response.text[:500]}"
                )
        except requests.RequestException as error:
            st.error(f"Could not connect to FastAPI: {error}")

