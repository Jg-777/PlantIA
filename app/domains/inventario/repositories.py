
from app.shared.database import db
from app.domains.inventario.models import Producto


class ProductoRepository:

    def list_all(self, category=None, search=None):
        query = Producto.query

        if category and category.lower() != "todos":
            query = query.filter(Producto.category.ilike(category))

        if search:
            query = query.filter(Producto.name.ilike(f"%{search}%"))

        return query.order_by(Producto.id.desc()).all()

    def get_by_id(self, producto_id: int):
        return db.session.get(Producto, producto_id)

    def create(self, producto: Producto):
        db.session.add(producto)
        db.session.commit()
        return producto

    def update(self, producto: Producto):
        db.session.commit()
        return producto

    def delete(self, producto: Producto):
        db.session.delete(producto)
        db.session.commit()

    def decrease_stock(self, producto: Producto, quantity: int):
        if producto.stock < quantity:
            return False

        producto.stock -= quantity
        db.session.commit()
        return True

