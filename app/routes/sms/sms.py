from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

sms = Blueprint("sms", __name__)


messages = [
    {
        "sender": "SBI Bank",
        "message": "Your account has been blocked. Verify immediately: http://sbi-secure-login.xyz",
        "answer": "phishing"
    },
    {
        "sender": "Amazon",
        "message": "Your package has been delivered successfully.",
        "answer": "safe"
    },
    {
        "sender": "Paytm",
        "message": "Congratulations! You won ₹50,000. Claim now: http://paytm-bonus.xyz",
        "answer": "phishing"
    },
    {
        "sender": "Government",
        "message": "Your Aadhaar KYC is expiring. Update today: http://aadhaar-update.xyz",
        "answer": "phishing"
    },
    {
        "sender": "Google",
        "message": "Your Google account password was changed successfully.",
        "answer": "safe"
    }
]


@sms.route("/")
@login_required
def home():
    return render_template(
        "sms/home.html",
        messages=messages,
        user=current_user
    )


@sms.route("/result", methods=["POST"])
@login_required
def result():

    correct = 0

    for i, sms_data in enumerate(messages):
        choice = request.form.get(f"q{i}")

        if choice == sms_data["answer"]:
            correct += 1

    score = int(correct / len(messages) * 100)

    simulation = Simulation(
        user_id=current_user.id,
        simulation_name="SMS Phishing",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "sms/result.html",
        score=score,
        correct=correct,
        total=len(messages),
        user=current_user
    )