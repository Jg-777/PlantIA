from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import create_app
from app.shared.database import db
from app.domains.auth.models import Usuario
from app.domains.inventario.models import Producto

load_dotenv()
app = create_app()

SEED_USERS = [
    {"username": "cliente", "name": "Cliente PlantIA", "role": "cliente", "password": "cliente123"},
    {"username": "ventas", "name": "Asesor de Ventas", "role": "ventas", "password": "ventas123"},
    {"username": "admin", "name": "Administrador PlantIA", "role": "admin", "password": "admin123"},
]

SEED_PRODUCTS = [
    {
        "name": "Fertilizante Equilibrado",
        "category": "Nutrición",
        "price": 28000,
        "stock": 20,
        "icon": "flask-conical",
        "image": "https://images.unsplash.com/photo-1628352081506-83c43123ed6d?auto=format&fit=crop&w=600&q=80",
        "description": "Aporte balanceado de nitrógeno, fósforo y potasio para plantas ornamentales.",
    },
    {
        "name": "Sustrato Universal Premium 5L",
        "category": "Sustratos",
        "price": 18000,
        "stock": 15,
        "icon": "layers",
        "image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=600&q=80",
        "description": "Mezcla rica en turba y perlita para mejorar la aireación y drenaje.",
    },
    {
        "name": "Jabón Potásico Ecológico 500ml",
        "category": "Control de plagas",
        "price": 22000,
        "stock": 12,
        "icon": "bug-off",
        "image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80",
        "description": "Elimina pulgones, cochinillas y araña roja sin dañar el ecosistema.",
    },
    {
        "name": "Humus de Lombriz Orgánico",
        "category": "Nutrición",
        "price": 16000,
        "stock": 25,
        "icon": "flower-2",
        "image": "https://images.unsplash.com/photo-1592417817098-8f3d6ef23a28?auto=format&fit=crop&w=600&q=80",
        "description": "Mejora la estructura del suelo y promueve un follaje verde y saludable.",
    },
    {
        "name": "Maceta Autorriego Minimalista",
        "category": "Herramientas",
        "price": 24000,
        "stock": 10,
        "icon": "box",
        "image": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=600&q=80",
        "description": "Con depósito interno para mantener la humedad ideal de tus raíces.",
    },
    {
        "name": "Tijera de Poda Ergonómica",
        "category": "Herramientas",
        "price": 32000,
        "stock": 18,
        "icon": "scissors",
        "image": "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?auto=format&fit=crop&w=600&q=80",
        "description": "Acero inoxidable para cortes limpios en tallos y esquejes.",
    },
]


def run_seed():
    with app.app_context():
        for u in SEED_USERS:
            exists = Usuario.query.filter_by(username=u["username"]).first()
            if not exists:
                db.session.add(
                    Usuario(
                        username=u["username"],
                        name=u["name"],
                        role=u["role"],
                        password_hash=generate_password_hash(u["password"]),
                    )
                )

        if Producto.query.count() == 0:
            for p in SEED_PRODUCTS:
                db.session.add(Producto(**p))

        db.session.commit()
        print("Seed completado correctamente.")


if __name__ == "__main__":
    run_seed()
