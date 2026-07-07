from flask import Blueprint, render_template
from flask_login import login_required, current_user

profile = Blueprint("profile", __name__)


@profile.route("/")
@login_required
def home():
    return render_template(
        "profile/profile.html",
        user=current_user
    )