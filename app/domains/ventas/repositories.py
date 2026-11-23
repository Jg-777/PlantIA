from app.shared.database import db
from app.domains.ventas.models import Venta


class VentaRepository:
    def create(self, venta: Venta) -> Venta:
        db.session.add(venta)
        db.session.commit()
        return venta

    def list_all(self, limit: int = 100):
        return Venta.query.order_by(Venta.created_at.desc()).limit(limit).all()

    def get_by_id(self, venta_id: int):
        return Venta.query.get(venta_id)