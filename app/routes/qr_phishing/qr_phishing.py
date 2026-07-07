from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

qr_phishing = Blueprint("qr_phishing", __name__)


questions = [
    {
        "image": "https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=https://google.com",
        "answer": "safe"
    },
    {
        "image": "https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=http://verify-paytm.xyz",
        "answer": "phishing"
    },
    {
        "image": "https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=https://amazon.in",
        "answer": "safe"
    },
    {
        "image": "https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=http://bank-login-security.xyz",
        "answer": "phishing"
    }
]


@qr_phishing.route("/")
@login_required
def home():
    return render_template(
        "qr_phishing/home.html",
        questions=questions,
        user=current_user
    )


@qr_phishing.route("/result", methods=["POST"])
@login_required
def result():

    correct = 0

    for i, q in enumerate(questions):

        choice = request.form.get(f"q{i}")

        if choice == q["answer"]:
            correct += 1

    score = int(correct / len(questions) * 100)

    simulation = Simulation(
        user_id=current_user.id,
        simulation_name="QR Code Phishing",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "qr_phishing/result.html",
        score=score,
        correct=correct,
        total=len(questions),
        user=current_user
    )