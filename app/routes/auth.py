from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.forms import RegisterForm, LoginForm
from app.models.user import User
from app.extensions import db

auth = Blueprint("auth", __name__)


# -----------------------------
# Register
# -----------------------------
@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(
                form.password.data
            )
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful!", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "register.html",
        form=form
    )


# -----------------------------
# Login
# -----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash("Welcome back!", "success")

            return redirect(url_for("dashboard.home"))

        flash("Invalid Email or Password", "danger")

    return render_template(
        "login.html",
        form=form
    )


# -----------------------------
# Logout
# -----------------------------
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "info")

    return redirect(url_for("main.home"))