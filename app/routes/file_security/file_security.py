from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

file_security = Blueprint("file_security", __name__)

attachments = [
    {
        "name": "Invoice.pdf",
        "safe": True
    },
    {
        "name": "Salary_Update.exe",
        "safe": False
    },
    {
        "name": "Meeting_Agenda.docx",
        "safe": True
    },
    {
        "name": "Photos.zip",
        "safe": True
    },
    {
        "name": "Resume.docm",
        "safe": False
    },
    {
        "name": "Windows_Update.scr",
        "safe": False
    },
    {
        "name": "Project_Report.pdf.exe",
        "safe": False
    },
    {
        "name": "Presentation.pptx",
        "safe": True
    }
]


@file_security.route("/")
@login_required
def home():
    return render_template(
        "file_security/home.html",
        attachments=attachments,
        user=current_user
    )


@file_security.route("/result", methods=["POST"])
@login_required
def result():

    correct = 0

    for i, item in enumerate(attachments):

        answer = request.form.get(f"q{i}")

        if (answer == "safe" and item["safe"]) or \
           (answer == "malicious" and not item["safe"]):

            correct += 1

    total = len(attachments)

    score = int((correct / total) * 100)

    simulation = Simulation(
        user_id=current_user.id,
        simulation_name="File Attachment Security",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "file_security/result.html",
        score=score,
        correct=correct,
        total=total,
        user=current_user
    )