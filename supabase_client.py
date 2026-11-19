"""Clientes da API do Supabase.

Um cliente novo é criado a cada chamada porque o cliente guarda a sessão
de quem fez login; compartilhar entre requisições misturaria usuários.
"""

from flask import current_app
from supabase import Client, create_client


def cliente_publico() -> Client:
    """Chave pública: usada no login (respeita o RLS)."""
    return create_client(
        current_app.config["SUPABASE_URL"],
        current_app.config["SUPABASE_PUBLISHABLE_KEY"],
    )


def cliente_admin() -> Client:
    """Chave secreta: só no servidor, para criar/editar/excluir contas no Auth."""
    return create_client(
        current_app.config["SUPABASE_URL"],
        current_app.config["SUPABASE_SECRET_KEY"],
    )
