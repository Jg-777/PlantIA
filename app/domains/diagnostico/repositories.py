
from app.shared.database import db
from app.domains.diagnostico.models import Diagnostico


class DiagnosticoRepository:

    def create(self, diagnostico: Diagnostico) -> Diagnostico:
        db.session.add(diagnostico)
        db.session.commit()
        return diagnostico

    def list_all(self, usuario_id=None, limit: int = 50):
        query = Diagnostico.query

        if usuario_id is not None:
            query = query.filter_by(usuario_id=usuario_id)

        return (
            query.order_by(Diagnostico.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_id(self, diagnostico_id: int):
        return Diagnostico.query.get(diagnostico_id)
