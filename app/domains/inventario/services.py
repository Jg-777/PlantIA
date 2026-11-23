
from app.domains.inventario.dtos import (
    CreateProductoDTO,
    UpdateProductoDTO,
)
from app.domains.inventario.models import Producto
from app.domains.inventario.repositories import ProductoRepository
from app.shared.exceptions import NotFoundException, ValidationException


class ProductoService:

    def __init__(self, repository: ProductoRepository = None):
        self.repository = repository or ProductoRepository()

    def list_products(self, category=None, search=None):
        return self.repository.list_all(
            category=category,
            search=search,
        )

    def get_product(self, producto_id: int):
        producto = self.repository.get_by_id(producto_id)

        if not producto:
            raise NotFoundException("Producto no encontrado.")

        return producto

    def create_product(self, dto: CreateProductoDTO):
        producto = Producto(
            name=dto.name,
            category=dto.category,
            price=dto.price,
            stock=dto.stock,
            icon=dto.icon,
            image=dto.image,
            description=dto.description,
        )

        return self.repository.create(producto)

    def update_product(self, producto_id: int, dto: UpdateProductoDTO):
        producto = self.get_product(producto_id)

        for field in (
            "name",
            "category",
            "price",
            "stock",
            "icon",
            "image",
            "description",
        ):
            value = getattr(dto, field)

            if value is not None:
                setattr(producto, field, value)

        return self.repository.update(producto)

    def delete_product(self, producto_id: int):
        producto = self.get_product(producto_id)
        self.repository.delete(producto)

    def increase_stock(self, producto_id: int, quantity: int):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValidationException(
                "La cantidad de entrada debe ser un entero mayor a cero."
            )

        producto = self.get_product(producto_id)

        producto.stock += quantity

        return self.repository.update(producto)

    def decrease_stock(self, producto_id: int, quantity: int):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValidationException(
                "La cantidad de salida debe ser un entero mayor a cero."
            )

        producto = self.get_product(producto_id)

        if producto.stock < quantity:
            raise ValidationException(
                f"Stock insuficiente para el producto {producto.name}."
            )

        producto.stock -= quantity

        return self.repository.update(producto)
