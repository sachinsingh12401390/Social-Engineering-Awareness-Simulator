from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.simulation import Simulation

email = Blueprint(
    "email",
    __name__,
    url_prefix="/email"
)


@email.route("/")
@login_required
def home():
    return render_template("simulations/email_home.html")


@email.route("/gmail")
@login_required
def gmail():
    return render_template("simulations/gmail.html")


@email.route("/result", methods=["GET", "POST"])
@login_required
def result():

    score = 100

    if request.method == "POST":
        email_address = request.form.get("email", "")
        password = request.form.get("password", "")

        if email_address == "" or password == "":
            score = 0

        simulation = Simulation(
            user_id=current_user.id,
            simulation_name="Phishing Email Simulation",
            score=score,
            status="Completed"
        )

        db.session.add(simulation)
        db.session.commit()

    return render_template(
        "simulations/result.html",
        score=score
    )