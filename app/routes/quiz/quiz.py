from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

quiz = Blueprint("quiz", __name__)


QUESTIONS = [
    {
        "question": "What is phishing?",
        "options": [
            "A cyber attack using fake emails",
            "A firewall",
            "An antivirus",
            "A programming language"
        ],
        "answer": 0
    },
    {
        "question": "Which password is the strongest?",
        "options": [
            "123456",
            "password",
            "Admin123",
            "P@ssw0rd!2026"
        ],
        "answer": 3
    },
    {
        "question": "HTTPS means a website is:",
        "options": [
            "Always safe",
            "Encrypted",
            "Fake",
            "Offline"
        ],
        "answer": 1
    },
    {
        "question": "What should you do if you receive a suspicious email?",
        "options": [
            "Click every link",
            "Reply immediately",
            "Report or delete it",
            "Forward it to everyone"
        ],
        "answer": 2
    },
    {
        "question": "Which one is malware?",
        "options": [
            "Virus",
            "Keyboard",
            "Printer",
            "Monitor"
        ],
        "answer": 0
    }
]


@quiz.route("/")
@login_required
def home():
    return render_template(
        "quiz/home.html",
        questions=QUESTIONS
    )


@quiz.route("/result", methods=["POST"])
@login_required
def result():

    score = 0

    for i, question in enumerate(QUESTIONS):
        answer = request.form.get(f"q{i}")

        if answer is not None and int(answer) == question["answer"]:
            score += 20

    simulation = Simulation(
        user_id=current_user.id,
        simulation_name="Cyber Security Quiz",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "quiz/result.html",
        score=score
    )