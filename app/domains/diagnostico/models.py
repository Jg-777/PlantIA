
from datetime import datetime, timezone

from app.shared.database import db


class Diagnostico(db.Model):
    __tablename__ = "diagnosticos"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True,
    )

    plant_name = db.Column(db.String(120), nullable=False)
    symptom = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    analysis = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "plant_name": self.plant_name,
            "symptom": self.symptom,
            "notes": self.notes or "",
            "image_filename": self.image_filename,
            "analysis": self.analysis,
            "created_at": self.created_at.isoformat(),
        }
