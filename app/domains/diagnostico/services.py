

import io
import time

from PIL import Image
from google import genai
from google.genai import errors

from app.domains.diagnostico.dtos import CreateDiagnosticoDTO
from app.domains.diagnostico.models import Diagnostico
from app.domains.diagnostico.repositories import DiagnosticoRepository
from app.shared.exceptions import ExternalServiceException, NotFoundException


class DiagnosticoService:
    def __init__(
        self,
        api_key: str,
        model_name: str,
        repository: DiagnosticoRepository = None,
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.repository = repository or DiagnosticoRepository()
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def _build_prompt(self, dto: CreateDiagnosticoDTO) -> str:
        return (
            "Actúa como un botánico experto y agrónomo. "
            "Analiza los datos y la fotografía de esta planta:\n"
            f"- Nombre ingresado: {dto.plant_name}\n"
            f"- Síntoma principal: {dto.symptom}\n"
            f"- Notas adicionales: {dto.notes or 'Ninguna'}\n\n"
            "Entrega una respuesta clara que contenga:\n"
            "1. Diagnóstico probable del problema.\n"
            "2. Explicación de sus posibles causas.\n"
            "3. Pasos prácticos y seguros para solucionarlo.\n"
            "4. Nivel de confianza y posibles alternativas.\n"
            "5. Recomendaciones para prevenir el problema.\n\n"
            "No afirmes un diagnóstico definitivo si la imagen o los datos "
            "no permiten identificar el problema con suficiente certeza. "
            "No inventes enfermedades ni tratamientos."
        )

    def create_and_analyze(self, dto: CreateDiagnosticoDTO) -> Diagnostico:
        if not self.client:
            raise ExternalServiceException(
                "La clave de API de Gemini no está configurada."
            )

        try:
            contents = [self._build_prompt(dto)]

            if dto.image_bytes:
                img = Image.open(io.BytesIO(dto.image_bytes))
                img.verify()

                img = Image.open(io.BytesIO(dto.image_bytes))
                img.load()
                contents.append(img)

            response = None

            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=contents,
                    )
                    break
                except errors.APIError as exc:
                    if exc.code == 503 and attempt < 2:
                        time.sleep(2 ** (attempt + 1))
                        continue
                    raise

            analysis_text = (response.text or "").strip()

            if not analysis_text:
                raise ExternalServiceException(
                    "Gemini no devolvió un análisis válido."
                )

            record = Diagnostico(
                usuario_id=dto.usuario_id,
                plant_name=dto.plant_name,
                symptom=dto.symptom,
                notes=dto.notes,
                image_filename=dto.image_filename,
                analysis=analysis_text,
            )

            return self.repository.create(record)

        except ExternalServiceException:
            raise
        except Exception as exc:
            raise ExternalServiceException(
                f"Error al consultar el servicio de IA: {exc}"
            )

    def list_diagnoses(self, usuario_id=None, limit: int = 50):
        return self.repository.list_all(
            usuario_id=usuario_id,
            limit=limit,
        )

    def get_diagnosis(self, diagnostico_id: int) -> Diagnostico:
        record = self.repository.get_by_id(diagnostico_id)

        if not record:
            raise NotFoundException("Diagnóstico no encontrado.")

        return record
