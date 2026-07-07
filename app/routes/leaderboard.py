from flask import Blueprint, render_template
from flask_login import login_required
from app.models.user import User

leaderboard = Blueprint(
    "leaderboard",
    __name__,
    url_prefix="/leaderboard"
)


@leaderboard.route("/")
@login_required
def home():
    users = User.query.all()

    leaderboard_data = []

    for user in users:
        total_score = sum(sim.score for sim in user.simulations)
        total_simulations = len(user.simulations)

        leaderboard_data.append({
            "name": user.name,
            "email": user.email,
            "score": total_score,
            "count": total_simulations
        })

    leaderboard_data.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return render_template(
        "leaderboard.html",
        leaderboard=leaderboard_data
    )