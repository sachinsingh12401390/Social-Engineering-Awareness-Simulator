from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.simulation import Simulation

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def home():

    simulations = (
        Simulation.query
        .filter_by(user_id=current_user.id)
        .order_by(Simulation.created_at.desc())
        .all()
    )

    total_simulations = len(simulations)

    average_score = (
        round(sum(sim.score for sim in simulations) / total_simulations, 2)
        if total_simulations > 0 else 0
    )

    completed = len(
        [s for s in simulations if s.status == "Completed"]
    )

    pending = total_simulations - completed

    return render_template(
        "dashboard.html",
        user=current_user,
        simulations=simulations,
        total_simulations=total_simulations,
        average_score=average_score,
        completed=completed,
        pending=pending
    )