from io import BytesIO
from datetime import datetime

from flask import send_file
from reportlab.lib.colors import darkblue
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.pdfbase import pdfmetrics


def generate_certificate(user):
    """
    Generate a PDF certificate for the given user.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = darkblue

    heading_style = styles["Heading2"]
    heading_style.alignment = TA_CENTER

    normal_style = styles["BodyText"]
    normal_style.alignment = TA_CENTER

    story = []

    story.append(Paragraph("Certificate of Completion", title_style))
    story.append(Spacer(1, 30))

    story.append(
        Paragraph(
            "This certificate is proudly presented to",
            heading_style,
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>{user.name}</b>",
            heading_style,
        )
    )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "For successfully completing the "
            "<b>Social Engineering Awareness Simulator</b>.",
            normal_style,
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Email: {user.email}",
            normal_style,
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Completion Date: {datetime.now().strftime('%d-%m-%Y')}",
            normal_style,
        )
    )

    story.append(Spacer(1, 10))

    certificate_id = f"SEA-{user.id:05d}"

    story.append(
        Paragraph(
            f"Certificate ID: {certificate_id}",
            normal_style,
        )
    )

    story.append(Spacer(1, 40))

    story.append(
        Paragraph(
            "<b>Authorized by</b>",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Cyber Security Awareness Team",
            normal_style,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="certificate.pdf",
        mimetype="application/pdf",
    )