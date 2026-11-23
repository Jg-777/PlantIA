
from flask import Blueprint, current_app, jsonify, request, g, abort

from app.domains.diagnostico.dtos import CreateDiagnosticoDTO
from app.domains.diagnostico.services import DiagnosticoService
from app.shared.security import auth_required


diagnostico_bp = Blueprint(
    "diagnostico",
    __name__,
    url_prefix="/api/diagnosticos",
)


def _get_service():
    return DiagnosticoService(
        api_key=current_app.config["GEMINI_API_KEY"],
        model_name=current_app.config["GEMINI_MODEL"],
    )


@diagnostico_bp.route("", methods=["POST"])
@auth_required
def create_diagnostico():
    dto = CreateDiagnosticoDTO.from_request(
        form_data=request.form,
        files_data=request.files,
        allowed_exts=current_app.config["ALLOWED_IMAGE_EXTENSIONS"],
        max_bytes=current_app.config["MAX_IMAGE_BYTES"],
        usuario_id=g.current_user["id"],
    )

    record = _get_service().create_and_analyze(dto)

    return jsonify({
        "success": True,
        "data": record.to_dict(),
        "analysis": record.analysis,
    }), 201


@diagnostico_bp.route("", methods=["GET"])
@auth_required
def list_diagnosticos():
    usuario_actual = g.current_user
    usuario_id = usuario_actual["id"]

    # Solo admin puede consultar el historial de otro usuario.
    if usuario_actual.get("role") == "admin":
        usuario_id = request.args.get("usuario_id", type=int) or usuario_id

    limit = request.args.get("limit", default=50, type=int)

    records = _get_service().list_diagnoses(
        usuario_id=usuario_id,
        limit=max(1, min(limit, 100)),
    )

    return jsonify({
        "success": True,
        "data": [record.to_dict() for record in records],
    }), 200


@diagnostico_bp.route("/<int:diagnostico_id>", methods=["GET"])
@auth_required
def get_diagnostico(diagnostico_id):
    record = _get_service().get_diagnosis(diagnostico_id)

    usuario_actual = g.current_user

    if (
        record.usuario_id != usuario_actual["id"]
        and usuario_actual.get("role") != "admin"
    ):
        abort(403)

    return jsonify({
        "success": True,
        "data": record.to_dict(),
    }), 200
