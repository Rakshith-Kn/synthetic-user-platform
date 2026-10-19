
import json
import re

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="Research Insights Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Insights & Experiment Results Dashboard")
st.caption(
    "Visual analysis of synthetic-user research experiments."
)

api_url = st.sidebar.text_input(
    "FastAPI URL",
    "http://127.0.0.1:8000",
).rstrip("/")


def parse_json(text, expected_type):
    result = json.loads(text)

    if not isinstance(result, expected_type):
        raise ValueError(
            f"Expected {expected_type.__name__} JSON."
        )

    return result


# Experiment details
st.header("Experiment Details")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input(
        "Product name",
        "CareSphere AI",
    )
    product_description = st.text_area(
        "Product description",
        "AI-powered healthcare and wellness platform",
    )
    scenario_name = st.text_input(
        "Scenario name",
        "Trust and Privacy Evaluation",
    )

with col2:
    objective = st.text_area(
        "Research objective",
        "Understand user trust, usefulness and usability.",
    )
    project_title = st.text_input(
        "Report title",
        "Synthetic User Research Report",
    )


# Paste actual API results
st.header("Research Data")

personas_text = st.text_area(
    "Persona profiles — JSON list",
    "[]",
    height=100,
)

survey_text = st.text_area(
    "Survey responses — JSON list",
    "[]",
    height=120,
)

interview_text = st.text_area(
    "Interview responses — JSON list",
    "[]",
    height=120,
)

insights_text = st.text_area(
    "Insight result — JSON object",
    '{"recurring_themes":[],"sentiment_breakdown":"Not provided","agreement_patterns":[],"behavioral_trends":[],"summary":""}',
    height=150,
)

would_use_text = st.text_area(
    "Would-use score result — JSON object",
    '{"persona_scores":[],"group_scores":[],"overall_score":null,"overall_reasoning":""}',
    height=120,
)

consistency_text = st.text_area(
    "Consistency results — JSON list",
    "[]",
    height=100,
)

validation_text = st.text_area(
    "Insight validation result — JSON object",
    '{"overall_validation_score":null,"overall_reasoning":"","strengths":[],"weaknesses":[],"recommendations":[]}',
    height=120,
)


# Validate the supplied JSON before displaying results
try:
    personas = parse_json(personas_text, list)
    survey = parse_json(survey_text, list)
    interviews = parse_json(interview_text, list)
    insights = parse_json(insights_text, dict)
    would_use = parse_json(would_use_text, dict)
    consistency = parse_json(consistency_text, list)
    validation = parse_json(validation_text, dict)

    # Accept wrapped API response structures too
    if isinstance(insights.get("insights"), dict):
        insights = insights["insights"]

    if isinstance(would_use.get("result"), dict):
        would_use = would_use["result"]

    if isinstance(validation.get("validation"), dict):
        validation = validation["validation"]

except (ValueError, TypeError, json.JSONDecodeError) as error:
    st.error(f"Please correct the JSON input: {error}")
    st.stop()


# Dashboard metrics
st.divider()
st.header("Research Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Personas", len(personas))
k2.metric("Survey responses", len(survey))
k3.metric("Interview turns", len(interviews))

overall_score = would_use.get("overall_score")

k4.metric(
    "Would-use score",
    f"{overall_score}/10"
    if isinstance(overall_score, (int, float))
    else "Not available",
)


# Theme clusters and sentiment
left, right = st.columns(2)

with left:
    st.subheader("Theme Clusters")

    themes = insights.get("recurring_themes", [])

    if themes:
        for index, theme in enumerate(themes, 1):
            st.markdown(f"**{index}. {theme}**")

            terms = set(
                re.findall(r"[a-zA-Z]{4,}", str(theme).lower())
            )

            responses = [
                str(item.get("response", item.get("answer", "")))
                for item in survey + interviews
                if isinstance(item, dict)
            ]

            # This is a rough keyword indicator, not a relevance score.
            hits = sum(
                any(term in response.lower() for term in terms)
                for response in responses
            )

            st.caption(
                f"Keyword overlap: {hits}/{len(responses)} responses"
            )
    else:
        st.info("No recurring themes supplied.")

with right:
    st.subheader("Sentiment Breakdown")
    st.write(
        insights.get(
            "sentiment_breakdown",
            "No sentiment result supplied.",
        )
    )

st.subheader("Agreement Patterns")
for item in insights.get("agreement_patterns", []):
    st.write("•", item)

st.subheader("Behavioral Trends")
for item in insights.get("behavioral_trends", []):
    st.write("•", item)


# Key persona quotes
st.subheader("Key Persona Quotes")

quotes = []

for response in survey + interviews:
    if not isinstance(response, dict):
        continue

    answer = response.get("response", response.get("answer", ""))

    if answer:
        name = response.get(
            "persona_name",
            response.get("persona_id", "Persona"),
        )
        quotes.append((name, answer))

if quotes:
    for name, quote in quotes[:12]:
        st.info(f"**{name}:** “{quote}”")
else:
    st.caption("No response quotes supplied.")


# Would-use individual and group scores
st.subheader("Product Adoption Scores")

persona_scores = would_use.get("persona_scores", [])

if persona_scores:
    score_data = [
        {
            "Persona": item.get("persona_id", "Unknown"),
            "Group": item.get("persona_group", "Unknown"),
            "Score": item.get("score", 0),
        }
        for item in persona_scores
    ]

    st.dataframe(score_data, use_container_width=True)

    st.bar_chart(
        pd.DataFrame(score_data).set_index("Persona")["Score"]
    )

group_scores = would_use.get("group_scores", [])

if group_scores:
    st.markdown("**Persona Group Scores**")

    group_data = [
        {
            "Persona Group": item.get("persona_group", "Unknown"),
            "Average Score": item.get("average_score", 0),
        }
        for item in group_scores
    ]

    st.dataframe(group_data, use_container_width=True)


# Insight validation scores
st.subheader("Insight Validation Scores")

score_fields = {
    key.replace("_", " ").title(): value
    for key, value in validation.items()
    if isinstance(value, (int, float))
    and (
        "score" in key
        or key.endswith(
            ("relevance", "coverage", "accuracy", "support", "attribution")
        )
    )
}

if score_fields:
    st.bar_chart(
        pd.Series(score_fields, name="Score out of 10")
    )

if validation.get("overall_reasoning"):
    st.write(validation["overall_reasoning"])

if validation.get("strengths"):
    st.markdown("**Strengths**")
    for item in validation["strengths"]:
        st.write("•", item)

if validation.get("weaknesses"):
    st.markdown("**Weaknesses**")
    for item in validation["weaknesses"]:
        st.write("•", item)

if validation.get("recommendations"):
    st.markdown("**Recommendations**")
    for item in validation["recommendations"]:
        st.write("•", item)


# Build the PDF request using the same displayed data
report_payload = {
    "project_title": project_title,
    "product_name": product_name,
    "product_description": product_description,
    "research_objective": objective,
    "scenario_name": scenario_name,
    "persona_profiles": personas,
    "survey_responses": survey,
    "interview_responses": interviews,
    "insight_summary": insights,
    "would_use_result": would_use,
    "consistency_results": consistency,
    "insight_validation": validation,
}

st.divider()
st.header("Research Report")

if st.button("Generate PDF Report", type="primary"):
    try:
        response = requests.post(
            f"{api_url}/research-report",
            json=report_payload,
            timeout=60,
        )

        if response.status_code == 200:
            if "application/pdf" in response.headers.get(
                "content-type", ""
            ):
                st.download_button(
                    "Download Research Report",
                    data=response.content,
                    file_name="synthetic_user_research_report.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("The API did not return a PDF.")
        else:
            st.error(
                f"API error {response.status_code}: "
                f"{response.text[:500]}"
            )

    except requests.RequestException as error:
        st.error(f"Cannot connect to FastAPI: {error}")
