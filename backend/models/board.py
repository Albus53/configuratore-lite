from .db import db

board_features = db.Table(
    "board_features",
    db.Column("board_id", db.String(64), db.ForeignKey("boards.id"), primary_key=True),
    db.Column(
        "feature_id",
        db.String(64),
        db.ForeignKey("features.id"),
        primary_key=True,
    ),
)


class Board(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    toolchain = db.Column(db.String(120), nullable=False)
    cross_compiler = db.Column(db.String(120), nullable=False)
    hardware_configuration = db.Column(db.JSON, nullable=True)

    features = db.relationship(
        "Feature",
        secondary=board_features,
        back_populates="boards",
        lazy="select",
    )

    def __repr__(self):
        return f"<Board {self.id}>"
