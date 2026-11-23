from app.shared.database import db
from app.shared.exceptions import NotFoundException
from app.domains.inventario.services import ProductoService
from app.domains.ventas.dtos import CreateVentaDTO
from app.domains.ventas.models import Venta, DetalleVenta
from app.domains.ventas.repositories import VentaRepository


class VentaService:
    def __init__(
        self,
        venta_repository: VentaRepository = None,
        producto_service: ProductoService = None,
    ):
        self.venta_repository = venta_repository or VentaRepository()
        self.producto_service = producto_service or ProductoService()

    def create_sale(self, dto: CreateVentaDTO, usuario_id=None) -> Venta:
        try:
            total = 0
            detalles = []

            for item in dto.items:
                producto = self.producto_service.decrease_stock(item.product_id, item.quantity)
                subtotal = producto.price * item.quantity
                total += subtotal
                detalles.append(
                    DetalleVenta(
                        producto_id=producto.id,
                        product_name=producto.name,
                        quantity=item.quantity,
                        unit_price=producto.price,
                        subtotal=subtotal,
                    )
                )

            venta = Venta(
                usuario_id=usuario_id,
                payment_method=dto.payment_method,
                total=total,
                items=detalles,
            )
            return self.venta_repository.create(venta)
        except Exception:
            db.session.rollback()
            raise

    def list_sales(self, limit: int = 100):
        return self.venta_repository.list_all(limit=limit)

    def get_sale(self, venta_id: int) -> Venta:
        venta = self.venta_repository.get_by_id(venta_id)
        if not venta:
            raise NotFoundException("Venta no encontrada.")
        return venta