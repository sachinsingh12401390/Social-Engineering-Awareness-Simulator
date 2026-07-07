from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

password = Blueprint("password", __name__)


@password.route("/")
@login_required
def home():
    return render_template(
        "password/password.html",
        user=current_user
    )


@password.route("/result", methods=["POST"])
@login_required
def result():

    password_text = request.form.get("password", "")

    score = 0
    feedback = []

    # Minimum length
    if len(password_text) >= 8:
        score += 20
    else:
        feedback.append("Password should contain at least 8 characters.")

    # Uppercase letter
    if any(c.isupper() for c in password_text):
        score += 20
    else:
        feedback.append("Add at least one uppercase letter.")

    # Lowercase letter
    if any(c.islower() for c in password_text):
        score += 20
    else:
        feedback.append("Add at least one lowercase letter.")

    # Number
    if any(c.isdigit() for c in password_text):
        score += 20
    else:
        feedback.append("Add at least one number.")

    # Special character
    if any(not c.isalnum() for c in password_text):
        score += 20
    else:
        feedback.append("Add at least one special character.")

    # Password strength
    if score == 100:
        strength = "Very Strong"
    elif score >= 80:
        strength = "Strong"
    elif score >= 60:
        strength = "Medium"
    elif score >= 40:
        strength = "Weak"
    else:
        strength = "Very Weak"

    # Save simulation result
    simulation = Simulation(
        user_id=current_user.id,
        simulation_name="Password Security",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "password/result.html",
        user=current_user,
        password=password_text,
        score=score,
        strength=strength,
        feedback=feedback
    )