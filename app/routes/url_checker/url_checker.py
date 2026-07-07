from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

url_checker = Blueprint("url_checker", __name__)


@url_checker.route("/")
@login_required
def home():
    return render_template(
        "url_checker/home.html",
        user=current_user
    )


@url_checker.route("/result", methods=["POST"])
@login_required
def result():

    url = request.form.get("url", "").strip().lower()

    score = 100
    risks = []

    suspicious_keywords = [
        "login",
        "verify",
        "secure",
        "update",
        "bank",
        "paypal",
        "account",
        "signin"
    ]

    if url.startswith("http://"):
        score -= 20
        risks.append("Uses HTTP instead of HTTPS.")

    if "@" in url:
        score -= 20
        risks.append("Contains '@' symbol.")

    if any(keyword in url for keyword in suspicious_keywords):
        score -= 20
        risks.append("Contains suspicious phishing keywords.")

    if any(char.isdigit() for char in url):
        score -= 10
        risks.append("Contains numeric characters.")

    if len(url) > 50:
        score -= 10
        risks.append("URL is unusually long.")

    if score < 0:
        score = 0

    if score >= 80:
        status = "Safe"
    elif score >= 50:
        status = "Suspicious"
    else:
        status = "High Risk"

    simulation = Simulation(
        user_id=current_user.id,
        simulation_name="URL Phishing Detection",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "url_checker/result.html",
        user=current_user,
        url=url,
        score=score,
        status=status,
        risks=risks
    )