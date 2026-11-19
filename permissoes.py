"""Controle de acesso por perfil (RF02), compartilhado pelas rotas."""

from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def exige_perfil(*perfis):
    """Libera a rota para os perfis informados. O admin tem acesso total (Fase 1)."""

    def decorador(funcao):
        @wraps(funcao)
        @login_required
        def verificar(*args, **kwargs):
            if current_user.perfil != "admin" and current_user.perfil not in perfis:
                abort(403)
            return funcao(*args, **kwargs)

        return verificar

    return decorador


def eh_admin() -> bool:
    return current_user.is_authenticated and current_user.perfil == "admin"
