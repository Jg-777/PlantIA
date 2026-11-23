from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, request

from app.shared.exceptions import (
    ForbiddenException,
    UnauthorizedException,
)


def create_access_token(user):
    """Genera un token JWT para un usuario autenticado."""
    payload = {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )


def auth_required(func):
    """Verifica que la solicitud tenga un token JWT válido."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "").strip()

        if not auth_header:
            raise UnauthorizedException("Debes iniciar sesión.")

        parts = auth_header.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
            raise UnauthorizedException("Formato de autorización inválido.")

        token = parts[1].strip()

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
            )

            if not payload.get("id"):
                raise UnauthorizedException("Token inválido.")

            g.current_user = {
                "id": payload["id"],
                "username": payload.get("username"),
                "role": payload.get("role"),
            }

        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Tu sesión ha expirado.")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("El token no es válido.")

        return func(*args, **kwargs)

    return wrapper


def roles_required(*allowed_roles):
    """Permite el acceso únicamente a los roles autorizados."""

    def decorator(func):

        @wraps(func)
        @auth_required
        def wrapper(*args, **kwargs):
            user_role = g.current_user.get("role")

            if user_role not in allowed_roles:
                raise ForbiddenException(
                    "No tienes permisos para realizar esta acción."
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
