
class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "APP_ERROR",
        details=None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details


class ValidationException(AppException):
    def __init__(self, message: str, details=None):
        super().__init__(
            message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class NotFoundException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message,
            status_code=404,
            error_code="NOT_FOUND",
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "No tienes autorización."):
        super().__init__(
            message,
            status_code=401,
            error_code="UNAUTHORIZED",
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "No tienes permisos para realizar esta acción."):
        super().__init__(
            message,
            status_code=403,
            error_code="FORBIDDEN",
        )


class ExternalServiceException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message,
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
        )
