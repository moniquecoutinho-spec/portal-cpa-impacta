"""Cria (ou redefine a senha de) os 4 usuários de teste no Supabase Auth.

As senhas NÃO ficam no código: o repositório é público. Cada execução gera
senhas aleatórias e as mostra uma única vez no terminal; guarde-as.

Uso, na raiz do projeto:
    python -m scripts.criar_usuarios_teste             # cria as contas que faltam
    python -m scripts.criar_usuarios_teste --redefinir # também troca a senha das existentes
"""

import secrets
import sys
from uuid import UUID

from app import app
from models import Perfil, Usuario, db
from supabase_client import cliente_admin

USUARIOS_TESTE = [
    ("Aluno Teste", "aluno@portal.com", "aluno"),
    ("Coordenador Teste", "coordenador@portal.com", "coordenador"),
    ("Avaliador Teste", "avaliador@portal.com", "avaliador"),
    ("Administrador CPA", "admin@portal.com", "admin"),
]


def nova_senha() -> str:
    return secrets.token_urlsafe(12)


def main(redefinir: bool = False):
    with app.app_context():
        admin = cliente_admin()
        for nome, email, perfil in USUARIOS_TESTE:
            existente = Usuario.query.filter_by(email=email).first()
            senha = nova_senha()

            if existente:
                if not redefinir:
                    print(f"já existe: {email} (use --redefinir para trocar a senha)")
                    continue
                admin.auth.admin.update_user_by_id(str(existente.id), {"password": senha})
                print(f"senha redefinida: {email}  ->  {senha}")
                continue

            resposta = admin.auth.admin.create_user(
                {
                    "email": email,
                    "password": senha,
                    "email_confirm": True,
                    "user_metadata": {"nome": nome},
                }
            )
            usuario = db.session.get(Usuario, UUID(resposta.user.id))
            usuario.perfil_id = Perfil.por_codigo_app(perfil).id
            db.session.commit()
            print(f"criado: {email} ({perfil})  ->  {senha}")


if __name__ == "__main__":
    main(redefinir="--redefinir" in sys.argv)
