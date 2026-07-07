from flask import Blueprint, render_template
from flask_login import login_required

from app.models.user import User
from app.models.simulation import Simulation

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/")
@login_required
def home():

    total_users = User.query.count()

    total_simulations = Simulation.query.count()

    completed = Simulation.query.filter_by(
        status="Completed"
    ).count()

    average_score = 0

    if total_simulations:
        total_score = sum(sim.score for sim in Simulation.query.all())
        average_score = round(total_score / total_simulations, 2)

    recent_simulations = Simulation.query.order_by(
        Simulation.created_at.desc()
    ).limit(10).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_simulations=total_simulations,
        completed=completed,
        average_score=average_score,
       recent_simulations=recent_simulations
    )