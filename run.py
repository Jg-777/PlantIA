
import os
from dotenv import load_dotenv

# Cargar las variables de entorno antes de importar Flask
load_dotenv()

from app import create_app


app = create_app()


if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"

    app.run(
        host=host,
        port=port,
        debug=debug,
    )
