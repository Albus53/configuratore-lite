from .db import db


class Feature(db.Model):
    __tablename__ = "features"

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    boards = db.relationship(
        "Board",
        secondary="board_features",
        back_populates="features",
        lazy="select",
    )

    def __repr__(self):
        return f"<Feature {self.id}>"
