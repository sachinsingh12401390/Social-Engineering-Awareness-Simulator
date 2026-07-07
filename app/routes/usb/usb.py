from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

usb = Blueprint("usb", __name__)

questions = [
    {
        "question": "You find a USB drive in your office parking lot. What should you do?",
        "options": [
            "Plug it into your office computer.",
            "Take it to the IT/Security department.",
            "Open it on your personal laptop.",
            "Give it to a coworker."
        ],
        "answer": 1
    },
    {
        "question": "Why are unknown USB drives dangerous?",
        "options": [
            "They may contain malware.",
            "They can steal credentials.",
            "They can automatically execute malicious code.",
            "All of the above."
        ],
        "answer": 3
    },
    {
        "question": "Which device should never be connected to your work PC?",
        "options": [
            "Company-issued USB",
            "Unknown USB drive",
            "Encrypted company USB",
            "Approved backup drive"
        ],
        "answer": 1
    },
    {
        "question": "Best practice when receiving an unknown USB?",
        "options": [
            "Scan it with antivirus first",
            "Use it immediately",
            "Throw it away or give it to IT",
            "Copy all files"
        ],
        "answer": 2
    }
]


@usb.route("/")
@login_required
def home():
    return render_template(
        "usb/home.html",
        questions=questions,
        user=current_user
    )


@usb.route("/result", methods=["POST"])
@login_required
def result():

    correct = 0

    for i, q in enumerate(questions):

        answer = request.form.get(f"q{i}")

        if answer and int(answer) == q["answer"]:
            correct += 1

    total = len(questions)
    score = int(correct / total * 100)

    simulation = Simulation(
        user_id=current_user.id,
        simulation_name="USB Drop Attack",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "usb/result.html",
        score=score,
        correct=correct,
        total=total,
        user=current_user
    )