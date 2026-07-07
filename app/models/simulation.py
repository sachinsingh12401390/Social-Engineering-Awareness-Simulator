from datetime import datetime

from app.extensions import db


class Simulation(db.Model):
    __tablename__ = "simulations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    simulation_name = db.Column(
        db.String(100),
        nullable=False
    )

    score = db.Column(
        db.Integer,
        default=0
    )

    status = db.Column(
        db.String(30),
        default="Completed"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Simulation {self.simulation_name} "
            f"User:{self.user_id} Score:{self.score}>"
        )