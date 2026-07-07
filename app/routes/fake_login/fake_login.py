from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

fake_login = Blueprint("fake_login", __name__)


@fake_login.route("/")
@login_required
def home():
    return render_template(
        "fake_login/home.html",
        user=current_user
    )


@fake_login.route("/gmail")
@login_required
def gmail():
    return render_template(
        "fake_login/gmail.html",
        platform="Google",
        user=current_user
    )


@fake_login.route("/facebook")
@login_required
def facebook():
    return render_template(
        "fake_login/facebook.html",
        platform="Facebook",
        user=current_user
    )


@fake_login.route("/instagram")
@login_required
def instagram():
    return render_template(
        "fake_login/instagram.html",
        platform="Instagram",
        user=current_user
    )


@fake_login.route("/result", methods=["POST"])
@login_required
def result():

    platform = request.form.get("platform")

    # We intentionally DO NOT store the submitted email or password.
    # This simulator is for awareness only.

    score = 100

    simulation = Simulation(
        user_id=current_user.id,
        simulation_name=f"{platform} Fake Login",
        score=score,
        status="Completed"
    )

    db.session.add(simulation)
    db.session.commit()

    return render_template(
        "fake_login/result.html",
        platform=platform,
        score=score,
        user=current_user
    )