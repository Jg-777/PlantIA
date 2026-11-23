


import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-desarrollo-plantaia")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-desarrollo-plantaia")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    MAX_IMAGE_BYTES = 8 * 1024 * 1024
