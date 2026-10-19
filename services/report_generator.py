
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def safe_text(value):
    if value is None:
        return "Not provided"

    if isinstance(value, (dict, list)):
        value = str(value)

    return escape(str(value)).replace("\n", "<br/>")


def add_heading(story, title, styles):
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(safe_text(title), styles["Heading2"]))
    story.append(Spacer(1, 2 * mm))


def add_list(story, items, styles):
    if not items:
        story.append(Paragraph("No data provided.", styles["Normal"]))
        return

    for item in items:
        if isinstance(item, dict):
            item = " | ".join(
                f"{key}: {value}" for key, value in item.items()
            )

        story.append(
            Paragraph("&#8226; " + safe_text(item), styles["Normal"])
        )
        story.append(Spacer(1, 2 * mm))


def build_research_report(data):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=data.get(
            "project_title",
            "Synthetic User Research Report"
        ),
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            textColor=colors.HexColor("#17324D"),
            alignment=1,
            spaceAfter=10,
        )
    )

    story = []

    # Report title
    story.append(
        Paragraph(
            safe_text(data.get("project_title")),
            styles["ReportTitle"],
        )
    )

    story.append(
        Paragraph(
            "Generated on " + datetime.now().strftime("%d %B %Y"),
            styles["Normal"],
        )
    )

    # 1. Experiment overview
    add_heading(story, "1. Experiment Overview", styles)

    overview = [
        ["Product", safe_text(data.get("product_name"))],
        ["Scenario", safe_text(data.get("scenario_name"))],
        [
            "Description",
            safe_text(data.get("product_description")),
        ],
        [
            "Research objective",
            safe_text(data.get("research_objective")),
        ],
    ]

    table = Table(overview, colWidths=[40 * mm, 130 * mm])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1),
             colors.HexColor("#EAF0F6")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(table)

    # 2. Personas
    add_heading(story, "2. Persona Profiles", styles)

    for index, persona in enumerate(
        data.get("persona_profiles", []), 1
    ):
        name = persona.get(
            "name",
            persona.get("persona_id", f"Persona {index}")
        )

        story.append(
            Paragraph(
                f"<b>{index}. {safe_text(name)}</b>",
                styles["Heading3"],
            )
        )

        story.append(
            Paragraph(safe_text(persona), styles["Normal"])
        )

        story.append(Spacer(1, 3 * mm))

    # 3. Survey responses
    add_heading(story, "3. Survey Response Highlights", styles)

    for response in data.get("survey_responses", []):
        name = response.get(
            "persona_name",
            response.get("persona_id", "Persona")
        )

        answer = response.get(
            "response",
            response.get("answer", "")
        )

        story.append(
            Paragraph(
                f"<b>{safe_text(name)}:</b> {safe_text(answer)}",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 2 * mm))

    # 4. Interview responses / quotes
    add_heading(story, "4. Interview Highlights", styles)

    for response in data.get("interview_responses", []):
        name = response.get(
            "persona_name",
            response.get("persona_id", "Persona")
        )

        answer = response.get(
            "response",
            response.get("answer", "")
        )

        story.append(
            Paragraph(
                f"<b>{safe_text(name)}:</b> "
                f"“{safe_text(answer)}”",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 2 * mm))

    # 5. Insights
    add_heading(story, "5. Research Insights", styles)

    insights = data.get("insight_summary", {})

    for label, key in [
        ("Recurring Themes", "recurring_themes"),
        ("Sentiment Breakdown", "sentiment_breakdown"),
        ("Agreement Patterns", "agreement_patterns"),
        ("Behavioral Trends", "behavioral_trends"),
        ("Summary", "summary"),
    ]:
        story.append(
            Paragraph(f"<b>{label}</b>", styles["Normal"])
        )

        value = insights.get(key, "Not provided")

        if isinstance(value, list):
            add_list(story, value, styles)
        else:
            story.append(
                Paragraph(safe_text(value), styles["Normal"])
            )

        story.append(Spacer(1, 2 * mm))

    # 6. Would-use scores
    add_heading(story, "6. Would-Use Product Scores", styles)

    scores = data.get("would_use_result", {})

    story.append(
        Paragraph(
            "<b>Overall score:</b> "
            + safe_text(scores.get("overall_score", "Not provided"))
            + " / 10",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            "<b>Reasoning:</b> "
            + safe_text(scores.get("overall_reasoning")),
            styles["Normal"],
        )
    )

    story.append(Paragraph("<b>Persona Scores</b>", styles["Normal"]))
    add_list(story, scores.get("persona_scores", []), styles)

    story.append(Paragraph("<b>Group Scores</b>", styles["Normal"]))
    add_list(story, scores.get("group_scores", []), styles)

    # 7. Consistency results
    add_heading(story, "7. Consistency Validation", styles)

    add_list(
        story,
        data.get("consistency_results", []),
        styles,
    )

    # 8. Insight validation
    add_heading(story, "8. Insight Validation", styles)

    validation = data.get("insight_validation", {})
    validation = validation.get("validation", validation)

    for key, value in validation.items():
        story.append(
            Paragraph(
                f"<b>{safe_text(key.replace('_', ' ').title())}:</b> "
                f"{safe_text(value)}",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 2 * mm))

    story.append(Spacer(1, 6 * mm))

    story.append(
        Paragraph(
            "Note: These findings are based on synthetic-user "
            "responses. Validate important conclusions with real "
            "users before making product decisions.",
            styles["Italic"],
        )
    )

    document.build(story)

    return buffer.getvalue()
