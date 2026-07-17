from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER


def create_pdf(
    filename,
    company,
    revenue,
    profit,
    roe,
    roce,
    score,
    recommendation,
    rating,
    risk
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    normal = styles["BodyText"]

    story = []

    story.append(
        Paragraph(
            "Nifty 100 Financial Analytics Report",
            title
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Company:</b> {company}",
            heading
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"Revenue : ₹ {revenue:,.0f} Cr",
            normal
        )
    )

    story.append(
        Paragraph(
            f"Net Profit : ₹ {profit:,.0f} Cr",
            normal
        )
    )

    story.append(
        Paragraph(
            f"ROE : {roe}%",
            normal
        )
    )

    story.append(
        Paragraph(
            f"ROCE : {roce}%",
            normal
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Financial Score :</b> {score}/100",
            heading
        )
    )

    story.append(
        Paragraph(
            f"<b>Recommendation :</b> {recommendation}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Rating :</b> {rating}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Risk :</b> {risk}",
            normal
        )
    )

    doc.build(story)