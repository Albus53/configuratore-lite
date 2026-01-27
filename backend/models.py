from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

# --------------
# USER MODEL
# --------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), default="client")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    builds = db.relationship("Build", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username} (ID: {self.id})>"

# ---------------
# BUILD MODEL
# ---------------
class Build(db.Model):
    __tablename__ = "builds"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(50), default="queued")
    configuration = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    finished_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Build {self.id} | Status: {self.status}>"