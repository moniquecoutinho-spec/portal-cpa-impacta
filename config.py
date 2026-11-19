"""Configuração do Flask lida do .env (nada sensível fica no código)."""

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

VARIAVEIS_OBRIGATORIAS = (
    "FLASK_SECRET_KEY",
    "SUPABASE_URL",
    "SUPABASE_PUBLISHABLE_KEY",
    "SUPABASE_SECRET_KEY",
)
VARIAVEIS_BANCO = ("SUPABASE_DB_HOST", "SUPABASE_DB_USER", "SUPABASE_DB_PASSWORD")


def _verificar_ambiente() -> None:
    """Falha com uma mensagem clara se faltar variável (ex.: não cadastrada na Vercel)."""
    faltando = [nome for nome in VARIAVEIS_OBRIGATORIAS if not os.getenv(nome)]
    if not os.getenv("DATABASE_URL"):
        faltando += [nome for nome in VARIAVEIS_BANCO if not os.getenv(nome)]
    if faltando:
        raise RuntimeError(
            "Variáveis de ambiente ausentes: "
            + ", ".join(faltando)
            + ". Defina-as no .env (local) ou nas Environment Variables da hospedagem."
        )


_verificar_ambiente()


def _url_banco() -> str:
    """Monta a URL do PostgreSQL do Supabase para o SQLAlchemy.

    Usa DATABASE_URL se existir (ex.: string do pooler do Supabase, necessária
    em hospedagens sem IPv6 como a Vercel). Caso contrário, monta a conexão
    direta a partir das variáveis SUPABASE_DB_*.
    """
    url = os.getenv("DATABASE_URL")
    if url:
        for prefixo in ("postgres://", "postgresql://"):
            if url.startswith(prefixo):
                return "postgresql+psycopg://" + url[len(prefixo) :]
        return url

    usuario = os.environ["SUPABASE_DB_USER"]
    senha = quote_plus(os.environ["SUPABASE_DB_PASSWORD"])
    host = os.environ["SUPABASE_DB_HOST"]
    porta = os.getenv("SUPABASE_DB_PORT", "5432")
    banco = os.getenv("SUPABASE_DB_NAME", "postgres")
    return f"postgresql+psycopg://{usuario}:{senha}@{host}:{porta}/{banco}?sslmode=require"


class Config:
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    # Limite do upload de PDF (o bucket aceita até 20 MB; folga para o formulário).
    MAX_CONTENT_LENGTH = 21 * 1024 * 1024

    # Cookie de sessão: inacessível ao JavaScript, não enviado em requisições de
    # outros sites e, em produção (a Vercel define VERCEL=1), só por HTTPS.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = bool(os.getenv("VERCEL"))

    # Proteção CSRF (Flask-WTF): o token vale enquanto durar a sessão.
    WTF_CSRF_TIME_LIMIT = None

    SQLALCHEMY_DATABASE_URI = _url_banco()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        # O pooler do Supabase em modo transação não aceita prepared statements.
        "connect_args": {"prepare_threshold": None},
    }

    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_PUBLISHABLE_KEY = os.environ["SUPABASE_PUBLISHABLE_KEY"]
    SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]
