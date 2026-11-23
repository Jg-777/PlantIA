from flask import Blueprint, jsonify, request, g
from app.domains.ventas.dtos import CreateVentaDTO
from app.domains.ventas.services import VentaService
from app.shared.security import auth_required, roles_required

ventas_bp = Blueprint("ventas", __name__, url_prefix="/api/ventas")


def _get_service() -> VentaService:
    return VentaService()


@ventas_bp.route("", methods=["POST"])
@auth_required
def create_venta():
    payload = request.get_json(silent=True) or {}
    dto = CreateVentaDTO.from_dict(payload)
    usuario_id = g.current_user["id"] if hasattr(g, "current_user") else None
    venta = _get_service().create_sale(dto, usuario_id=usuario_id)
    return jsonify({
        "success": True,
        "data": venta.to_dict(),
    }), 201


@ventas_bp.route("", methods=["GET"])
@roles_required("admin", "ventas")
def list_ventas():
    limit = request.args.get("limit", default=100, type=int)
    ventas = _get_service().list_sales(limit=limit)
    return jsonify({
        "success": True,
        "data": [v.to_dict() for v in ventas],
    }), 200


@ventas_bp.route("/<int:venta_id>", methods=["GET"])
@auth_required
def get_venta(venta_id: int):
    venta = _get_service().get_sale(venta_id)
    return jsonify({
        "success": True,
        "data": venta.to_dict(),
    }), 200