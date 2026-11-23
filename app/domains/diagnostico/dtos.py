
from dataclasses import dataclass
from typing import Optional

from app.shared.exceptions import ValidationException


VALID_SYMPTOMS = {
    "manchas",
    "amarillas",
    "plaga",
    "marchita",
    "crecimiento",
    "otro",
}


@dataclass
class CreateDiagnosticoDTO:
    plant_name: str
    symptom: str
    notes: str
    image_bytes: Optional[bytes] = None
    image_filename: Optional[str] = None
    usuario_id: Optional[int] = None

    @classmethod
    def from_request(
        cls,
        form_data,
        files_data,
        allowed_exts,
        max_bytes,
        usuario_id=None,
    ):
        plant_name = (
            form_data.get("plantName") or "Planta sin identificar"
        ).strip()

        symptom = (form_data.get("symptom") or "otro").strip().lower()
        notes = (form_data.get("notes") or "").strip()

        if len(plant_name) > 120:
            raise ValidationException(
                "El nombre de la planta no puede superar 120 caracteres."
            )

        if symptom not in VALID_SYMPTOMS:
            raise ValidationException("Síntoma no válido.")

        if len(notes) > 2000:
            raise ValidationException(
                "Las observaciones no pueden superar 2000 caracteres."
            )

        image_bytes = None
        image_filename = None

        image_file = files_data.get("photo")

        if image_file and image_file.filename:
            filename = image_file.filename.strip()
            ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

            if ext not in allowed_exts:
                raise ValidationException(
                    "Formato de imagen no permitido. Usa JPG, PNG o WEBP."
                )

            image_bytes = image_file.read()

            if not image_bytes:
                raise ValidationException("La imagen está vacía.")

            if len(image_bytes) > max_bytes:
                raise ValidationException(
                    "La imagen supera el tamaño máximo permitido."
                )

            image_filename = filename

        return cls(
            plant_name=plant_name,
            symptom=symptom,
            notes=notes,
            image_bytes=image_bytes,
            image_filename=image_filename,
            usuario_id=usuario_id,
        )
