from datetime import datetime, timezone

from .db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), default="admin")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    builds = db.relationship("Build", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username} (ID: {self.id})>"
