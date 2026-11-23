
from flask import Blueprint, jsonify, request, g

from app.domains.auth.dtos import RegisterDTO, LoginDTO
from app.domains.auth.services import AuthService
from app.shared.security import auth_required


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth",
)


def _get_service():
    return AuthService()


@auth_bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True) or {}
    dto = RegisterDTO.from_dict(payload)

    usuario = _get_service().register(dto)

    return jsonify({
        "success": True,
        "message": "Usuario registrado correctamente.",
        "data": usuario.to_dict(),
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    dto = LoginDTO.from_dict(payload)

    result = _get_service().login(dto)

    return jsonify({
        "success": True,
        "data": result,
    }), 200


@auth_bp.route("/me", methods=["GET"])
@auth_required
def me():
    usuario_id = g.current_user["id"]
    usuario = _get_service().get_current_user(usuario_id)

    return jsonify({
        "success": True,
        "data": usuario.to_dict(),
    }), 200
