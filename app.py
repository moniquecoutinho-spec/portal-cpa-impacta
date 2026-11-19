from datetime import date
from urllib.parse import urlparse
from uuid import UUID

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required
from flask_wtf.csrf import CSRFError, CSRFProtect
from sqlalchemy import text

from config import Config
from models import PERFIS_VALIDOS, Avaliacao, Documento, Participacao, Perfil, Usuario, db
from permissoes import exige_perfil
from routes.autenticacao import autenticacao
from routes.dashboards import dashboards
from routes.publico import publico
from supabase_client import cliente_admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
# Todo POST precisa do token CSRF (campo csrf_token nos formulários ou cabeçalho X-CSRFToken).
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "autenticacao.login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.login_message_category = "info"


@login_manager.user_loader
def carregar_usuario(usuario_id):
    try:
        usuario = db.session.get(Usuario, UUID(usuario_id))
    except ValueError:
        return None
    # Conta desativada pelo admin perde a sessão na próxima requisição.
    return usuario if usuario and usuario.ativo else None


app.register_blueprint(autenticacao)
app.register_blueprint(publico)
app.register_blueprint(dashboards)


@app.errorhandler(403)
def acesso_negado(_erro):
    return render_template(
        "erro.html",
        codigo=403,
        titulo="Acesso negado",
        mensagem="Seu perfil não tem permissão para acessar esta página.",
    ), 403


@app.errorhandler(404)
def nao_encontrado(_erro):
    return render_template(
        "erro.html",
        codigo=404,
        titulo="Página não encontrada",
        mensagem="O endereço não existe ou o conteúdo foi removido.",
    ), 404


@app.errorhandler(CSRFError)
def token_invalido(_erro):
    flash("A página expirou ou o envio não veio do portal. Tente novamente.", "danger")
    origem = request.referrer or ""
    # Só volta para a página anterior se ela for do próprio portal (evita redirecionamento aberto).
    if urlparse(origem).netloc != request.host:
        origem = url_for("publico.inicio")
    return redirect(origem)


@app.errorhandler(413)
def arquivo_grande(_erro):
    flash("O arquivo enviado passa do limite permitido.", "danger")
    return redirect(url_for("publico.relatorios"))


# -----------------------------------------------------------------------------
# Saúde: confirma que o Flask está conectado ao banco do Supabase
# -----------------------------------------------------------------------------
@app.route("/saude")
def saude():
    try:
        db.session.execute(text("select 1"))
        return {"app": "ok", "banco": "ok", "perfis": Perfil.query.count()}
    except Exception as erro:  # noqa: BLE001 - endpoint de diagnóstico
        return {"app": "ok", "banco": "erro", "detalhe": type(erro).__name__}, 503


# -----------------------------------------------------------------------------
# Endereços antigos dos protótipos: mantidos para não quebrar links salvos.
# -----------------------------------------------------------------------------
@app.route("/modelo1")
@app.route("/modelo2")
@app.route("/modelo3")
@login_required
def modelos_antigos():
    return redirect(url_for("dashboards.listar"))


# -----------------------------------------------------------------------------
# Aluno
# -----------------------------------------------------------------------------
@app.route("/aluno/avaliacoes")
@exige_perfil("aluno")
def aluno_avaliacoes():
    avaliacoes = Avaliacao.query.order_by(Avaliacao.data_inicio.desc()).all()
    return render_template("AlunoAvaliacoes.html", avaliacoes=avaliacoes)


# -----------------------------------------------------------------------------
# Coordenador
# -----------------------------------------------------------------------------
def _ler_periodo():
    """Lê título e datas do formulário. Retorna None e avisa se for inválido."""
    titulo = request.form.get("titulo", "").strip()
    inicio = request.form.get("inicio", "")
    fim = request.form.get("fim", "")

    if not titulo or not inicio or not fim:
        flash("Preencha todos os campos.", "danger")
        return None

    try:
        data_inicio = date.fromisoformat(inicio)
        data_fim = date.fromisoformat(fim)
    except ValueError:
        flash("Datas inválidas.", "danger")
        return None

    if data_fim < data_inicio:
        flash("A data de encerramento não pode ser anterior à data de início.", "danger")
        return None

    return titulo, data_inicio, data_fim


@app.route("/coordenador", methods=["GET", "POST"])
@exige_perfil("coordenador")
def coordenador():
    if request.method == "POST":
        dados = _ler_periodo()
        if dados:
            titulo, data_inicio, data_fim = dados
            db.session.add(Avaliacao(titulo=titulo, data_inicio=data_inicio, data_fim=data_fim))
            db.session.commit()
            flash("Avaliação cadastrada com sucesso!", "success")
        return redirect(url_for("coordenador"))

    total_alunos = Usuario.query_por_perfil("aluno").filter(Usuario.ativo.is_(True)).count()
    total_participacoes = Participacao.query.filter_by(respondida=True).count()
    percentual = round(total_participacoes / total_alunos * 100, 1) if total_alunos else 0

    return render_template(
        "Coordenador.html",
        avaliacoes=Avaliacao.query.order_by(Avaliacao.id.desc()).all(),
        total_avaliacoes=Avaliacao.query.count(),
        total_alunos=total_alunos,
        total_participacoes=total_participacoes,
        percentual_participacao=percentual,
        total_documentos=Documento.query.count(),
    )


@app.route("/coordenador/avaliacao/<int:avaliacao_id>/editar", methods=["GET", "POST"])
@exige_perfil("coordenador")
def editar_avaliacao(avaliacao_id):
    avaliacao = db.session.get(Avaliacao, avaliacao_id)
    if not avaliacao:
        flash("Avaliação não encontrada.", "danger")
        return redirect(url_for("coordenador"))

    if request.method == "POST":
        dados = _ler_periodo()
        status = request.form.get("status", "")
        if dados and not status:
            flash("Preencha todos os campos.", "danger")
        if not dados or not status:
            return redirect(url_for("editar_avaliacao", avaliacao_id=avaliacao.id))

        avaliacao.titulo, avaliacao.data_inicio, avaliacao.data_fim = dados
        avaliacao.status = status
        db.session.commit()

        flash("Avaliação atualizada com sucesso!", "success")
        return redirect(url_for("coordenador"))

    return render_template("EditarAvaliacao.html", avaliacao=avaliacao)


@app.route("/coordenador/avaliacao/<int:avaliacao_id>/excluir", methods=["POST"])
@exige_perfil("coordenador")
def excluir_avaliacao(avaliacao_id):
    avaliacao = db.session.get(Avaliacao, avaliacao_id)
    if not avaliacao:
        flash("Avaliação não encontrada.", "danger")
        return redirect(url_for("coordenador"))

    db.session.delete(avaliacao)
    db.session.commit()
    flash("Avaliação excluída com sucesso!", "success")
    return redirect(url_for("coordenador"))


# -----------------------------------------------------------------------------
# Administrador (contas ficam no Supabase Auth)
# -----------------------------------------------------------------------------
def _destino_admin():
    return "admin_escuro" if request.form.get("tema") == "escuro" else "admin"


def _cadastrar_usuario(destino):
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    perfil = request.form.get("perfil", "")

    if not nome or not email or not senha or not perfil:
        flash("Preencha todos os campos.", "danger")
    elif perfil not in PERFIS_VALIDOS:
        flash("Perfil inválido.", "danger")
    elif Usuario.query.filter_by(email=email).first():
        flash("Este e-mail já está cadastrado.", "danger")
    else:
        # Cria a conta no Supabase Auth; o trigger do banco cria a linha em
        # public.usuarios como "aluno". Em seguida definimos o perfil escolhido.
        resposta = cliente_admin().auth.admin.create_user(
            {
                "email": email,
                "password": senha,
                "email_confirm": True,
                "user_metadata": {"nome": nome},
            }
        )
        novo = db.session.get(Usuario, UUID(resposta.user.id))
        novo.perfil_id = Perfil.por_codigo_app(perfil).id
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")

    return redirect(url_for(destino))


def _painel_admin(template):
    busca = request.args.get("busca", "").strip()
    perfil_filtro = request.args.get("perfil", "").strip()

    consulta = Usuario.query
    if busca:
        consulta = consulta.filter(
            db.or_(Usuario.nome.ilike(f"%{busca}%"), Usuario.email.ilike(f"%{busca}%"))
        )
    if perfil_filtro in PERFIS_VALIDOS:
        consulta = consulta.join(Perfil).filter(
            Perfil.id == Perfil.por_codigo_app(perfil_filtro).id
        )

    return render_template(
        template,
        usuarios=consulta.order_by(Usuario.nome.asc()).all(),
        total_usuarios=Usuario.query.count(),
        total_alunos=Usuario.query_por_perfil("aluno").count(),
        total_coordenadores=Usuario.query_por_perfil("coordenador").count(),
        total_avaliadores=Usuario.query_por_perfil("avaliador").count(),
        total_administradores=Usuario.query_por_perfil("admin").count(),
        total_inativos=Usuario.query.filter_by(ativo=False).count(),
    )


@app.route("/admin", methods=["GET", "POST"])
@exige_perfil("admin")
def admin():
    if request.method == "POST":
        return _cadastrar_usuario("admin")
    return _painel_admin("Admin.html")


@app.route("/admin/escuro", methods=["GET", "POST"])
@exige_perfil("admin")
def admin_escuro():
    if request.method == "POST":
        return _cadastrar_usuario("admin_escuro")
    return _painel_admin("AdminEscuro.html")


@app.route("/admin/usuario/<uuid:usuario_id>/alternar", methods=["POST"])
@exige_perfil("admin")
def alternar_usuario(usuario_id):
    destino = _destino_admin()
    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        flash("Usuário não encontrado.", "danger")
    elif usuario.id == current_user.id:
        flash("Você não pode desativar sua própria conta.", "danger")
    else:
        usuario.ativo = not usuario.ativo
        db.session.commit()
        estado = "ativado" if usuario.ativo else "desativado"
        flash(f"Usuário {estado} com sucesso!", "success")

    return redirect(url_for(destino))


@app.route("/admin/usuario/<uuid:usuario_id>/excluir", methods=["POST"])
@exige_perfil("admin")
def excluir_usuario(usuario_id):
    destino = _destino_admin()
    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        flash("Usuário não encontrado.", "danger")
    elif usuario.id == current_user.id:
        flash("Você não pode excluir sua própria conta.", "danger")
    else:
        # Excluir no Auth remove a linha de public.usuarios em cascata.
        cliente_admin().auth.admin.delete_user(str(usuario.id))
        db.session.expire_all()
        flash("Usuário excluído com sucesso!", "success")

    return redirect(url_for(destino))


@app.route("/admin/usuario/<uuid:usuario_id>/editar", methods=["GET", "POST"])
@exige_perfil("admin")
def editar_usuario(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for("admin"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        perfil = request.form.get("perfil", "")
        senha = request.form.get("senha", "")

        if not nome or not email or perfil not in PERFIS_VALIDOS:
            flash("Verifique os campos obrigatórios.", "danger")
            return redirect(url_for("editar_usuario", usuario_id=usuario.id))

        em_uso = Usuario.query.filter(Usuario.email == email, Usuario.id != usuario.id).first()
        if em_uso:
            flash("Este e-mail já está sendo utilizado.", "danger")
            return redirect(url_for("editar_usuario", usuario_id=usuario.id))

        # E-mail e senha pertencem ao Supabase Auth.
        dados_auth = {}
        if email != usuario.email:
            dados_auth["email"] = email
        if senha:
            dados_auth["password"] = senha
        if dados_auth:
            cliente_admin().auth.admin.update_user_by_id(str(usuario.id), dados_auth)

        usuario.nome = nome
        usuario.email = email
        usuario.perfil_id = Perfil.por_codigo_app(perfil).id
        db.session.commit()

        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for(_destino_admin()))

    return render_template(
        "EditarUsuario.html", usuario=usuario, tema=request.args.get("tema", "claro")
    )


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
