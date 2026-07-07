from flask import Flask

from config import Config
from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Import models
    from app.models import User, Simulation

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.simulations.email import email
    from app.routes.admin import admin
    from app.routes.leaderboard import leaderboard
    from app.routes.certificate import certificate
    from app.routes.profile.profile import profile
    from app.routes.password.password import password
    from app.routes.quiz.quiz import quiz
    from app.routes.url_checker.url_checker import url_checker
    from app.routes.fake_login.fake_login import fake_login
    from app.routes.sms.sms import sms
    from app.routes.qr_phishing.qr_phishing import qr_phishing
    from app.routes.file_security.file_security import file_security
    from app.routes.usb.usb import usb

    # IMPORTANT: import the Blueprint object
    from app.routes.analytics.analytics import analytics

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)

    app.register_blueprint(email, url_prefix="/email")
    app.register_blueprint(password, url_prefix="/password")
    app.register_blueprint(quiz, url_prefix="/quiz")

    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(leaderboard, url_prefix="/leaderboard")
    app.register_blueprint(certificate, url_prefix="/certificate")
    app.register_blueprint(profile, url_prefix="/profile")
    app.register_blueprint(url_checker, url_prefix="/url-checker")
    app.register_blueprint(fake_login, url_prefix="/fake-login")
    app.register_blueprint(sms, url_prefix="/sms")
    app.register_blueprint(qr_phishing, url_prefix="/qr-phishing")
    app.register_blueprint(file_security, url_prefix="/file-security")
    app.register_blueprint(usb, url_prefix="/usb")
    app.register_blueprint(analytics, url_prefix="/analytics")

    with app.app_context():
        db.create_all()

    return app