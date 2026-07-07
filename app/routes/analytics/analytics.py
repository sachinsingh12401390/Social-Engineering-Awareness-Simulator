from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.simulation import Simulation

# Blueprint
analytics = Blueprint("analytics", __name__)


@analytics.route("/")
@login_required
def home():
    # Get all simulations for the logged-in user
    simulations = Simulation.query.filter_by(
        user_id=current_user.id
    ).all()

    labels = []
    scores = []

    # Collect simulation names and scores
    for sim in simulations:
        labels.append(sim.simulation_name)
        scores.append(sim.score)

    total = len(scores)

    if total > 0:
        average = round(sum(scores) / total, 2)
        highest = max(scores)
    else:
        average = 0
        highest = 0

    return render_template(
        "analytics/dashboard.html",
        user=current_user,
        labels=labels,
        scores=scores,
        total=total,
        average=average,
        highest=highest
    )