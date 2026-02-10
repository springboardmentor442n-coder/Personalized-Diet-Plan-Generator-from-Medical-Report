from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_diet_pdf(age, gender, values, conditions, risks, ai_diet):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Personalized Diet Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Age:</b> {age}", styles["Normal"]))
    story.append(Paragraph(f"<b>Gender:</b> {gender}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Lab Values</b>", styles["Heading2"]))
    for k, v in values.items():
        story.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Detected Conditions</b>", styles["Heading2"]))
    for c in conditions:
        story.append(Paragraph(f"- {c}", styles["Normal"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Health Risks</b>", styles["Heading2"]))
    for k, v in risks.items():
        story.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>7-Day AI Diet Plan</b>", styles["Heading2"]))
    for line in ai_diet.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer
