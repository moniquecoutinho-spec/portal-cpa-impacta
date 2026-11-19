from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from supabase import AuthError

from models import Usuario, db
from supabase_client import cliente_publico

autenticacao = Blueprint("autenticacao", __name__)


@autenticacao.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        try:
            # A senha é validada pelo Supabase Auth (hash bcrypt no auth.users).
            resposta = cliente_publico().auth.sign_in_with_password(
                {"email": email, "password": senha}
            )
        except AuthError:
            resposta = None

        usuario = db.session.get(Usuario, resposta.user.id) if resposta and resposta.user else None

        if usuario and usuario.ativo:
            login_user(usuario)
            flash("Login realizado com sucesso!", "success")
            # Todos os perfis entram pela área de dashboards; o menu leva às demais áreas.
            return redirect(url_for("dashboards.listar"))

        flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html")


@autenticacao.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("publico.inicio"))


@autenticacao.route("/minha-conta")
@login_required
def minha_conta():
    return {"nome": current_user.nome, "perfil": current_user.perfil}
