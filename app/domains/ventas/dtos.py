from dataclasses import dataclass
from typing import List
from app.shared.exceptions import ValidationException

VALID_PAYMENT_METHODS = {
    "Efectivo",
    "Nequi / Daviplata",
    "Tarjeta",
    "Transferencia",
}


@dataclass
class VentaItemDTO:
    product_id: int
    quantity: int


@dataclass
class CreateVentaDTO:
    payment_method: str
    items: List[VentaItemDTO]

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict):
            raise ValidationException("El cuerpo de la petición debe ser un JSON válido.")

        payment_method = (data.get("payment_method") or "").strip()
        if payment_method not in VALID_PAYMENT_METHODS:
            raise ValidationException(
                f"Método de pago no válido. Opciones: {', '.join(sorted(VALID_PAYMENT_METHODS))}."
            )

        raw_items = data.get("items")
        if not isinstance(raw_items, list) or len(raw_items) == 0:
            raise ValidationException("Debes enviar al menos un producto en 'items'.")

        parsed_items = []
        for entry in raw_items:
            if not isinstance(entry, dict):
                raise ValidationException("Cada elemento de 'items' debe ser un objeto.")
            try:
                product_id = int(entry.get("product_id"))
                quantity = int(entry.get("quantity"))
            except (TypeError, ValueError):
                raise ValidationException("'product_id' y 'quantity' deben ser números enteros.")

            if product_id <= 0 or quantity <= 0:
                raise ValidationException("'product_id' y 'quantity' deben ser mayores a 0.")

            parsed_items.append(VentaItemDTO(product_id=product_id, quantity=quantity))

        return cls(payment_method=payment_method, items=parsed_items)