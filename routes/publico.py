"""Área pública (RN01: nunca exige login) e a gestão do admin feita nas mesmas telas.

Páginas: início, mural de devolutivas, relatórios e boletins, contato.
"""

import os
import re
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from uuid import uuid4

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user
from werkzeug.utils import secure_filename

from models import (
    CATEGORIAS_DOCUMENTO,
    STATUS_DEVOLUTIVA,
    Avaliacao,
    Dashboard,
    Devolutiva,
    Documento,
    db,
)
from permissoes import exige_perfil
from supabase_client import cliente_admin

publico = Blueprint("publico", __name__)

BUCKET = "documentos"
LIMITE_PDF = 20 * 1024 * 1024  # igual ao file_size_limit do bucket
# Formato dos caminhos gerados por _novo_caminho: "2026/1a2b3c4d-nome.pdf".
CAMINHO_PDF = re.compile(r"\d{4}/[0-9a-f]{8}-[A-Za-z0-9._-]+\.pdf")


def url_documento(documento: Documento) -> str:
    """URL pública do PDF no Storage (bucket público, leitura liberada pela RLS)."""
    base = current_app.config["SUPABASE_URL"].rstrip("/")
    return f"{base}/storage/v1/object/public/{BUCKET}/{documento.storage_path}"


# -----------------------------------------------------------------------------
# Início
# -----------------------------------------------------------------------------
@publico.route("/")
def inicio():
    indicadores = {
        "devolutivas": Devolutiva.query.count(),
        "concluidas": Devolutiva.query.filter_by(status="concluido").count(),
        "documentos": Documento.query.count(),
        "dashboards": Dashboard.query.filter_by(ativo=True).count(),
        "avaliacoes": Avaliacao.query.count(),
    }
    recentes = Devolutiva.query.order_by(Devolutiva.data_publicacao.desc()).limit(3).all()
    return render_template("index.html", indicadores=indicadores, recentes=recentes)


# -----------------------------------------------------------------------------
# Mural de devolutivas (RF05 público, RF06 admin)
# -----------------------------------------------------------------------------
def _ler_devolutiva():
    dados = {
        "titulo": request.form.get("titulo", "").strip(),
        "area_responsavel": request.form.get("area_responsavel", "").strip(),
        "acao": request.form.get("acao", "").strip(),
        "status": request.form.get("status", ""),
        "data_publicacao": request.form.get("data_publicacao", ""),
    }
    if not all(dados.values()):
        flash("Preencha todos os campos da devolutiva.", "danger")
        return None
    if dados["status"] not in STATUS_DEVOLUTIVA:
        flash("Status inválido.", "danger")
        return None
    try:
        dados["data_publicacao"] = date.fromisoformat(dados["data_publicacao"])
    except ValueError:
        flash("Data de publicação inválida.", "danger")
        return None
    return dados


@publico.route("/devolutivas")
def devolutivas():
    status = request.args.get("status", "")
    consulta = Devolutiva.query
    if status in STATUS_DEVOLUTIVA:
        consulta = consulta.filter_by(status=status)
    lista = consulta.order_by(Devolutiva.data_publicacao.desc(), Devolutiva.id.desc()).all()
    return render_template(
        "devolutivas.html",
        devolutivas=lista,
        status_opcoes=STATUS_DEVOLUTIVA,
        status_filtro=status,
        hoje=date.today().isoformat(),
    )


@publico.route("/devolutivas", methods=["POST"])
@exige_perfil("admin")
def criar_devolutiva():
    dados = _ler_devolutiva()
    if dados:
        db.session.add(Devolutiva(**dados, created_by=current_user.id))
        db.session.commit()
        flash("Devolutiva publicada no mural.", "success")
    return redirect(url_for("publico.devolutivas"))


@publico.route("/devolutivas/<int:devolutiva_id>/editar", methods=["GET", "POST"])
@exige_perfil("admin")
def editar_devolutiva(devolutiva_id):
    devolutiva = db.get_or_404(Devolutiva, devolutiva_id)
    if request.method == "POST":
        dados = _ler_devolutiva()
        if not dados:
            return redirect(url_for("publico.editar_devolutiva", devolutiva_id=devolutiva.id))
        for campo, valor in dados.items():
            setattr(devolutiva, campo, valor)
        db.session.commit()
        flash("Devolutiva atualizada.", "success")
        return redirect(url_for("publico.devolutivas"))
    return render_template(
        "devolutiva_form.html", devolutiva=devolutiva, status_opcoes=STATUS_DEVOLUTIVA
    )


@publico.route("/devolutivas/<int:devolutiva_id>/excluir", methods=["POST"])
@exige_perfil("admin")
def excluir_devolutiva(devolutiva_id):
    db.session.delete(db.get_or_404(Devolutiva, devolutiva_id))
    db.session.commit()
    flash("Devolutiva removida do mural.", "success")
    return redirect(url_for("publico.devolutivas"))


# -----------------------------------------------------------------------------
# Relatórios e boletins (RF07 público, RF08 admin, RN04 só PDF)
# -----------------------------------------------------------------------------
@publico.route("/relatorios")
def relatorios():
    categoria = request.args.get("categoria", "")
    ano = request.args.get("ano", "")

    consulta = Documento.query
    if categoria in CATEGORIAS_DOCUMENTO:
        consulta = consulta.filter_by(categoria=categoria)
    if ano.isdigit():
        consulta = consulta.filter_by(ano_referencia=int(ano))

    anos = [
        linha[0]
        for linha in db.session.query(Documento.ano_referencia)
        .distinct()
        .order_by(Documento.ano_referencia.desc())
    ]
    lista = consulta.order_by(Documento.ano_referencia.desc(), Documento.id.desc()).all()
    return render_template(
        "relatorios.html",
        documentos=lista,
        categorias=CATEGORIAS_DOCUMENTO,
        anos=anos,
        categoria_filtro=categoria,
        ano_filtro=ano,
        ano_atual=date.today().year,
        url_documento=url_documento,
    )


def _ano_valido(ano: str) -> bool:
    return ano.isdigit() and 2000 <= int(ano) <= 2100


def _novo_caminho(ano: str, nome_arquivo: str) -> str:
    nome = re.sub(r"\.pdf$", "", secure_filename(nome_arquivo), flags=re.I) or "documento"
    return f"{ano}/{uuid4().hex[:8]}-{nome}.pdf"


def _caminho_enviado_valido(caminho: str, ano: str) -> bool:
    """Confere um PDF enviado direto ao Storage pelo navegador.

    O caminho precisa ter o formato gerado por _novo_caminho e o arquivo precisa
    existir e começar com a assinatura %PDF (RN04). Lê só os primeiros bytes.
    """
    if not CAMINHO_PDF.fullmatch(caminho) or not caminho.startswith(f"{ano}/"):
        return False
    if Documento.query.filter_by(storage_path=caminho).first():
        return False
    base = current_app.config["SUPABASE_URL"].rstrip("/")
    pedido = Request(
        f"{base}/storage/v1/object/public/{BUCKET}/{quote(caminho)}",
        headers={"Range": "bytes=0-3"},
    )
    try:
        with urlopen(pedido, timeout=10) as resposta:  # noqa: S310 - URL do próprio Supabase
            return resposta.read(4) == b"%PDF"
    except (HTTPError, URLError, TimeoutError):
        return False


@publico.route("/relatorios/assinatura", methods=["POST"])
@exige_perfil("admin")
def assinar_envio():
    """Gera uma URL de envio de uso único para o navegador mandar o PDF direto ao Storage.

    Assim o arquivo não passa pelo Flask, e o limite de ~4,5 MB por requisição da
    Vercel deixa de valer: o limite passa a ser o do bucket (20 MB).
    """
    dados = request.get_json(silent=True) or {}
    nome = str(dados.get("nome", ""))
    ano = str(dados.get("ano", ""))
    if not nome.lower().endswith(".pdf"):
        return jsonify(erro="Envie apenas arquivos PDF."), 400
    if not _ano_valido(ano):
        return jsonify(erro="Ano de referência inválido."), 400

    caminho = _novo_caminho(ano, nome)
    assinatura = cliente_admin().storage.from_(BUCKET).create_signed_upload_url(caminho)
    return jsonify(url=assinatura["signed_url"], caminho=caminho)


@publico.route("/relatorios", methods=["POST"])
@exige_perfil("admin")
def enviar_documento():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip() or None
    categoria = request.form.get("categoria", "")
    ano = request.form.get("ano_referencia", "")
    # Com JavaScript, o PDF já foi para o Storage e chega só o caminho;
    # sem JavaScript, o arquivo vem no formulário (limitado a ~4,5 MB na Vercel).
    caminho_enviado = request.form.get("storage_path", "").strip()
    arquivo = request.files.get("arquivo")
    tem_arquivo = bool(caminho_enviado or (arquivo and arquivo.filename))

    erro = None
    if not titulo or not ano or not tem_arquivo:
        erro = "Preencha o título, o ano e escolha o arquivo PDF."
    elif categoria not in CATEGORIAS_DOCUMENTO:
        erro = "Categoria inválida."
    elif not _ano_valido(ano):
        erro = "Ano de referência inválido."
    if erro:
        flash(erro, "danger")
        return redirect(url_for("publico.relatorios"))

    armazenamento = cliente_admin().storage.from_(BUCKET)
    if caminho_enviado:
        if not _caminho_enviado_valido(caminho_enviado, ano):
            ja_cadastrado = Documento.query.filter_by(storage_path=caminho_enviado).first()
            if CAMINHO_PDF.fullmatch(caminho_enviado) and not ja_cadastrado:
                armazenamento.remove([caminho_enviado])  # descarta o arquivo inválido
            flash("Envie apenas arquivos PDF.", "danger")
            return redirect(url_for("publico.relatorios"))
        caminho = caminho_enviado
    else:
        conteudo = arquivo.read()
        # RN04: confere a extensão e a assinatura do arquivo, não só o nome.
        if not arquivo.filename.lower().endswith(".pdf") or not conteudo.startswith(b"%PDF"):
            flash("Envie apenas arquivos PDF.", "danger")
            return redirect(url_for("publico.relatorios"))
        if len(conteudo) > LIMITE_PDF:
            flash("O PDF passa do limite de 20 MB.", "danger")
            return redirect(url_for("publico.relatorios"))
        caminho = _novo_caminho(ano, arquivo.filename)
        armazenamento.upload(caminho, conteudo, {"content-type": "application/pdf"})

    db.session.add(
        Documento(
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
            ano_referencia=int(ano),
            storage_path=caminho,
            created_by=current_user.id,
        )
    )
    db.session.commit()
    flash("Documento publicado.", "success")
    return redirect(url_for("publico.relatorios"))


@publico.route("/relatorios/<int:documento_id>/excluir", methods=["POST"])
@exige_perfil("admin")
def excluir_documento(documento_id):
    documento = db.get_or_404(Documento, documento_id)
    cliente_admin().storage.from_(BUCKET).remove([documento.storage_path])
    db.session.delete(documento)
    db.session.commit()
    flash("Documento removido.", "success")
    return redirect(url_for("publico.relatorios"))


# -----------------------------------------------------------------------------
# Contato (RF09)
# -----------------------------------------------------------------------------
@publico.route("/contato")
def contato():
    canais = {
        "chat": os.getenv("CPA_LINK_CHAT", "https://chat.google.com/"),
        "meet": os.getenv("CPA_LINK_MEET", "https://meet.google.com/"),
        "email": os.getenv("CPA_EMAIL", "cpa@faculdadeimpacta.edu.br"),
    }
    return render_template("contato.html", canais=canais)
