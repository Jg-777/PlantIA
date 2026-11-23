
from dataclasses import dataclass
from typing import Optional

from app.shared.exceptions import ValidationException


@dataclass
class CreateProductoDTO:
    name: str
    category: str
    price: int
    stock: int
    icon: str = "sprout"
    image: str = ""
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict):
            raise ValidationException("Debes enviar un JSON válido.")

        name = (data.get("name") or "").strip()
        category = (data.get("category") or "").strip()

        if not 2 <= len(name) <= 120:
            raise ValidationException("El nombre debe tener entre 2 y 120 caracteres.")

        if not 2 <= len(category) <= 80:
            raise ValidationException("La categoría debe tener entre 2 y 80 caracteres.")

        try:
            price = int(data.get("price"))
            stock = int(data.get("stock"))
        except (TypeError, ValueError):
            raise ValidationException("El precio y el stock deben ser números enteros.")

        if price < 0 or stock < 0:
            raise ValidationException("El precio y el stock no pueden ser negativos.")

        return cls(
            name=name,
            category=category,
            price=price,
            stock=stock,
            icon=(data.get("icon") or "sprout").strip(),
            image=(data.get("image") or "").strip(),
            description=(data.get("description") or "").strip(),
        )


@dataclass
class UpdateProductoDTO:
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict):
            raise ValidationException("Debes enviar un JSON válido.")

        dto = cls()

        if "name" in data:
            value = (data.get("name") or "").strip()
            if not 2 <= len(value) <= 120:
                raise ValidationException("El nombre debe tener entre 2 y 120 caracteres.")
            dto.name = value

        if "category" in data:
            value = (data.get("category") or "").strip()
            if not 2 <= len(value) <= 80:
                raise ValidationException("La categoría debe tener entre 2 y 80 caracteres.")
            dto.category = value

        for field in ("price", "stock"):
            if field in data:
                try:
                    value = int(data[field])
                except (TypeError, ValueError):
                    raise ValidationException(f"{field} debe ser un número entero.")

                if value < 0:
                    raise ValidationException(f"{field} no puede ser negativo.")

                setattr(dto, field, value)

        if "icon" in data:
            dto.icon = (data.get("icon") or "sprout").strip()

        if "image" in data:
            dto.image = (data.get("image") or "").strip()

        if "description" in data:
            dto.description = (data.get("description") or "").strip()

        return dto
