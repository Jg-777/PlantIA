
from dataclasses import dataclass

from app.shared.exceptions import ValidationException


@dataclass
class RegisterDTO:
    username: str
    name: str
    password: str

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValidationException("Debes enviar los datos del usuario.")

        username = str(data.get("username", "")).strip()
        name = str(data.get("name", "")).strip()
        password = data.get("password", "")

        if not username or len(username) < 3 or len(username) > 80:
            raise ValidationException(
                "El usuario debe tener entre 3 y 80 caracteres."
            )

        if not name or len(name) < 2 or len(name) > 120:
            raise ValidationException(
                "El nombre debe tener entre 2 y 120 caracteres."
            )

        if not isinstance(password, str) or len(password) < 8 or len(password) > 128:
            raise ValidationException(
                "La contraseña debe tener entre 8 y 128 caracteres."
            )

        return cls(
            username=username,
            name=name,
            password=password,
        )


@dataclass
class LoginDTO:
    username: str
    password: str

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValidationException("Debes enviar los datos de inicio de sesión.")

        username = str(data.get("username", "")).strip()
        password = data.get("password", "")

        if not username or not isinstance(password, str) or not password:
            raise ValidationException(
                "Debes ingresar el usuario y la contraseña."
            )

        return cls(
            username=username,
            password=password,
        )
