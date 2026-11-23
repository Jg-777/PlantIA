
from app import create_app
from app.shared.database import db
from app.domains.inventario.models import Producto


PRODUCTOS = [
    # ABONOS
    {
        "name": "Humus de lombriz 1 kg",
        "category": "abonos",
        "price": 18000,
        "stock": 35,
        "icon": "sprout",
        "description": "Abono orgánico natural que mejora la fertilidad del suelo."
    },
    {
        "name": "Abono NPK 15-15-15 1 kg",
        "category": "abonos",
        "price": 25000,
        "stock": 25,
        "icon": "flask-conical",
        "description": "Fertilizante equilibrado para el crecimiento de las plantas."
    },
    {
        "name": "Abono líquido universal 500 ml",
        "category": "abonos",
        "price": 22000,
        "stock": 30,
        "icon": "droplets",
        "description": "Fertilizante líquido para plantas ornamentales."
    },
    {
        "name": "Abono para floración 1 kg",
        "category": "abonos",
        "price": 28000,
        "stock": 20,
        "icon": "flower-2",
        "description": "Fertilizante formulado para apoyar la etapa de floración."
    },
    {
        "name": "Harina de hueso 1 kg",
        "category": "abonos",
        "price": 16000,
        "stock": 18,
        "icon": "sprout",
        "description": "Enmienda orgánica que aporta fósforo y calcio."
    },
    {
        "name": "Abono orgánico compost 2 kg",
        "category": "abonos",
        "price": 20000,
        "stock": 28,
        "icon": "leaf",
        "description": "Materia orgánica compostada para mejorar el suelo."
    },

    # SUSTRATOS
    {
        "name": "Tierra abonada 5 kg",
        "category": "sustratos",
        "price": 15000,
        "stock": 40,
        "icon": "sprout",
        "description": "Mezcla de tierra preparada para plantas de jardín."
    },
    {
        "name": "Fibra de coco 1 kg",
        "category": "sustratos",
        "price": 18000,
        "stock": 25,
        "icon": "leaf",
        "description": "Sustrato ligero que ayuda a retener humedad."
    },
    {
        "name": "Perlita 1 litro",
        "category": "sustratos",
        "price": 12000,
        "stock": 30,
        "icon": "layers",
        "description": "Material que mejora la aireación y el drenaje."
    },
    {
        "name": "Vermiculita 1 litro",
        "category": "sustratos",
        "price": 14000,
        "stock": 20,
        "icon": "layers",
        "description": "Sustrato mineral que ayuda a conservar la humedad."
    },
    {
        "name": "Sustrato para cactus 2 kg",
        "category": "sustratos",
        "price": 19000,
        "stock": 22,
        "icon": "cactus",
        "description": "Mezcla de buen drenaje para cactus y suculentas."
    },
    {
        "name": "Corteza de pino 2 kg",
        "category": "sustratos",
        "price": 17000,
        "stock": 18,
        "icon": "tree-pine",
        "description": "Material utilizado en mezclas para plantas ornamentales."
    },

    # CONTROL DE PLAGAS
    {
        "name": "Jabón potásico 500 ml",
        "category": "plagas",
        "price": 22000,
        "stock": 25,
        "icon": "spray-can",
        "description": "Producto para el manejo de determinadas plagas vegetales."
    },
    {
        "name": "Aceite de neem 250 ml",
        "category": "plagas",
        "price": 28000,
        "stock": 20,
        "icon": "droplets",
        "description": "Producto de origen vegetal para el manejo de plagas."
    },
    {
        "name": "Trampas adhesivas amarillas x10",
        "category": "plagas",
        "price": 12000,
        "stock": 35,
        "icon": "bug",
        "description": "Trampas para monitorear insectos voladores."
    },
    {
        "name": "Tierra de diatomeas 500 g",
        "category": "plagas",
        "price": 18000,
        "stock": 20,
        "icon": "shield-check",
        "description": "Producto mineral utilizado en el manejo de algunas plagas."
    },
    {
        "name": "Insecticida para plantas 500 ml",
        "category": "plagas",
        "price": 26000,
        "stock": 15,
        "icon": "spray-can",
        "description": "Producto para el control de plagas según las indicaciones de su etiqueta."
    },
    {
        "name": "Fungicida para plantas 250 ml",
        "category": "plagas",
        "price": 24000,
        "stock": 15,
        "icon": "shield-check",
        "description": "Producto para el manejo de enfermedades causadas por hongos."
    },

    # HERRAMIENTAS
    {
        "name": "Tijeras de poda",
        "category": "herramientas",
        "price": 28000,
        "stock": 20,
        "icon": "scissors",
        "description": "Herramienta para podar ramas pequeñas y hojas."
    },
    {
        "name": "Pala de jardinería",
        "category": "herramientas",
        "price": 15000,
        "stock": 25,
        "icon": "shovel",
        "description": "Pala manual para remover y trasladar sustrato."
    },
    {
        "name": "Rociador manual 1 litro",
        "category": "herramientas",
        "price": 18000,
        "stock": 30,
        "icon": "spray-can",
        "description": "Pulverizador manual para aplicar agua y soluciones."
    },
    {
        "name": "Guantes de jardinería",
        "category": "herramientas",
        "price": 16000,
        "stock": 25,
        "icon": "hand",
        "description": "Guantes para proteger las manos durante las labores de jardinería."
    },
    {
        "name": "Kit de herramientas 3 piezas",
        "category": "herramientas",
        "price": 35000,
        "stock": 12,
        "icon": "wrench",
        "description": "Kit básico para el cuidado y mantenimiento de plantas."
    },
    {
        "name": "Regadera de jardín 2 litros",
        "category": "herramientas",
        "price": 24000,
        "stock": 18,
        "icon": "droplets",
        "description": "Regadera manual para el riego de plantas."
    },

    # MACETAS
    {
        "name": "Maceta plástica pequeña",
        "category": "macetas",
        "price": 8000,
        "stock": 40,
        "icon": "flower-2",
        "description": "Maceta pequeña para plantas ornamentales."
    },
    {
        "name": "Maceta plástica mediana",
        "category": "macetas",
        "price": 14000,
        "stock": 35,
        "icon": "flower-2",
        "description": "Maceta mediana para plantas de interior y exterior."
    },
    {
        "name": "Maceta de barro 15 cm",
        "category": "macetas",
        "price": 18000,
        "stock": 20,
        "icon": "flower-2",
        "description": "Maceta de barro para plantas ornamentales."
    },
    {
        "name": "Maceta colgante",
        "category": "macetas",
        "price": 22000,
        "stock": 18,
        "icon": "flower-2",
        "description": "Maceta colgante para plantas decorativas."
    },
    {
        "name": "Maceta autorregante",
        "category": "macetas",
        "price": 32000,
        "stock": 12,
        "icon": "droplets",
        "description": "Maceta con depósito que facilita el suministro de agua."
    },
    {
        "name": "Maceta de cerámica decorativa",
        "category": "macetas",
        "price": 38000,
        "stock": 10,
        "icon": "flower-2",
        "description": "Maceta decorativa para plantas de interior."
    }
]


def seed_productos():
    app = create_app()

    with app.app_context():
        agregados = 0
        existentes = 0

        try:
            for datos in PRODUCTOS:
                nombre = datos["name"].strip().lower()

                producto_existente = Producto.query.filter(
                    db.func.lower(Producto.name) == nombre
                ).first()

                if producto_existente:
                    existentes += 1
                    print(f"YA EXISTE: {datos['name']}")
                    continue

                producto = Producto(**datos)
                db.session.add(producto)
                agregados += 1

            db.session.commit()

            print("\n========== RESULTADO ==========")
            print(f"Productos nuevos: {agregados}")
            print(f"Productos que ya existían: {existentes}")
            print(f"Total del catálogo: {len(PRODUCTOS)}")

        except Exception as error:
            db.session.rollback()
            print("\nERROR: No se pudieron guardar los productos.")
            print(error)
            raise


if __name__ == "__main__":
    seed_productos()
