from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.services.certificate_service import generate_certificate

certificate = Blueprint("certificate", __name__)


@certificate.route("/")
@login_required
def home():
    return render_template(
        "certificate.html",
        user=current_user
    )


@certificate.route("/download")
@login_required
def download():
    return generate_certificate(current_user)