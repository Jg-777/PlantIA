
from app.shared.database import db
from app.domains.auth.models import Usuario


class UsuarioRepository:

    def get_by_username(self, username):
        return Usuario.query.filter_by(username=username).first()

    def get_by_id(self, usuario_id):
        return db.session.get(Usuario, usuario_id)

    def create(self, usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario
