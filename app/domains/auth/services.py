
from werkzeug.security import generate_password_hash, check_password_hash

from app.domains.auth.models import Usuario
from app.domains.auth.repositories import UsuarioRepository
from app.domains.auth.dtos import RegisterDTO, LoginDTO
from app.shared.security import create_access_token
from app.shared.exceptions import (
    ValidationException,
    UnauthorizedException,
)


class AuthService:

    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()

    def register(self, dto: RegisterDTO):
        existing_user = self.repository.get_by_username(dto.username)

        if existing_user:
            raise ValidationException("Ese nombre de usuario ya está registrado.")

        usuario = Usuario(
            username=dto.username,
            name=dto.name,
            role="cliente",
            password_hash=generate_password_hash(dto.password),
        )

        return self.repository.create(usuario)

    def login(self, dto: LoginDTO):
        usuario = self.repository.get_by_username(dto.username)

        if not usuario or not check_password_hash(
            usuario.password_hash,
            dto.password,
        ):
            raise UnauthorizedException("Usuario o contraseña incorrectos.")

        token = create_access_token(usuario)

        return {
            "token": token,
            "user": usuario.to_dict(),
        }

    def get_current_user(self, usuario_id):
        usuario = self.repository.get_by_id(usuario_id)

        if not usuario:
            raise UnauthorizedException("El usuario ya no existe.")

        return usuario
