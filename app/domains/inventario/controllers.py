
from flask import Blueprint, jsonify, request

from app.domains.inventario.dtos import (
    CreateProductoDTO,
    UpdateProductoDTO,
)
from app.domains.inventario.services import ProductoService
from app.shared.security import roles_required


inventario_bp = Blueprint(
    "inventario",
    __name__,
    url_prefix="/api/productos",
)


def _get_service():
    return ProductoService()


@inventario_bp.route("", methods=["GET"])
def list_productos():
    category = request.args.get("category")
    search = request.args.get("search")

    productos = _get_service().list_products(
        category=category,
        search=search,
    )

    return jsonify({
        "success": True,
        "data": [p.to_dict() for p in productos],
    }), 200


@inventario_bp.route("/<int:producto_id>", methods=["GET"])
def get_producto(producto_id):
    producto = _get_service().get_product(producto_id)

    return jsonify({
        "success": True,
        "data": producto.to_dict(),
    }), 200


@inventario_bp.route("", methods=["POST"])
@roles_required("admin", "ventas")
def create_producto():
    payload = request.get_json(silent=True) or {}
    dto = CreateProductoDTO.from_dict(payload)

    producto = _get_service().create_product(dto)

    return jsonify({
        "success": True,
        "data": producto.to_dict(),
    }), 201


@inventario_bp.route("/<int:producto_id>", methods=["PUT"])
@roles_required("admin", "ventas")
def update_producto(producto_id):
    payload = request.get_json(silent=True) or {}
    dto = UpdateProductoDTO.from_dict(payload)

    producto = _get_service().update_product(
        producto_id,
        dto,
    )

    return jsonify({
        "success": True,
        "data": producto.to_dict(),
    }), 200


@inventario_bp.route("/<int:producto_id>", methods=["DELETE"])
@roles_required("admin")
def delete_producto(producto_id):
    _get_service().delete_product(producto_id)

    return jsonify({
        "success": True,
        "message": "Producto eliminado correctamente.",
    }), 200
