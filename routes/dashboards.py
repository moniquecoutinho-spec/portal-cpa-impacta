"""Área restrita: dashboards do Looker Studio por perfil (RF03) e gestão dos links (RF04)."""

import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Dashboard, Perfil, db
from permissoes import exige_perfil

dashboards = Blueprint("dashboards", __name__)

# O mesmo domínio aceito pelo CHECK da tabela dashboards.
URL_VALIDA = re.compile(r"^https://(lookerstudio|datastudio)\.google\.com/")
# Perfis que dependem de vínculo; admin e avaliador MEC veem todos por regra (RN03).
PERFIS_VINCULAVEIS = {"aluno": "Aluno", "coordenador": "Coordenador"}


def normalizar_url(url: str) -> str:
    """Aceita o link de compartilhamento e converte para o link de incorporação."""
    url = url.strip()
    if "/reporting/" in url and "/embed/" not in url:
        url = url.replace("/reporting/", "/embed/reporting/", 1)
    return url


def _ler_formulario():
    nome = request.form.get("nome", "").strip()
    url = normalizar_url(request.form.get("url_embed", ""))
    if not nome or not url:
        flash("Informe o nome e o link do dashboard.", "danger")
        return None
    if not URL_VALIDA.match(url):
        flash("O link precisa ser do Looker Studio (lookerstudio.google.com).", "danger")
        return None
    ordem = request.form.get("ordem", "0")
    perfis = [p for p in request.form.getlist("perfis") if p in PERFIS_VINCULAVEIS]
    return {
        "nome": nome,
        "descricao": request.form.get("descricao", "").strip() or None,
        "url_embed": url,
        "ativo": request.form.get("ativo") == "on",
        "ordem": int(ordem) if ordem.lstrip("-").isdigit() else 0,
        "perfis": [Perfil.por_codigo_app(p) for p in perfis],
    }


def _proximo_codigo() -> str:
    numeros = [
        int(c[5:]) for (c,) in db.session.query(Dashboard.codigo) if re.fullmatch(r"DASH-\d+", c)
    ]
    return f"DASH-{max(numeros, default=0) + 1:02d}"


@dashboards.route("/dashboards")
@login_required
def listar():
    return render_template(
        "dashboards.html",
        dashboards=Dashboard.visiveis_para(current_user.perfil).all(),
        perfis_vinculaveis=PERFIS_VINCULAVEIS,
    )


@dashboards.route("/dashboards", methods=["POST"])
@exige_perfil("admin")
def criar():
    dados = _ler_formulario()
    if dados:
        db.session.add(Dashboard(codigo=_proximo_codigo(), updated_by=current_user.id, **dados))
        db.session.commit()
        flash("Dashboard cadastrado.", "success")
    return redirect(url_for("dashboards.listar"))


@dashboards.route("/dashboards/<int:dashboard_id>/editar", methods=["GET", "POST"])
@exige_perfil("admin")
def editar(dashboard_id):
    dashboard = db.get_or_404(Dashboard, dashboard_id)
    if request.method == "POST":
        dados = _ler_formulario()
        if not dados:
            return redirect(url_for("dashboards.editar", dashboard_id=dashboard.id))
        for campo, valor in dados.items():
            setattr(dashboard, campo, valor)
        dashboard.updated_by = current_user.id
        db.session.commit()
        flash("Dashboard atualizado.", "success")
        return redirect(url_for("dashboards.listar"))
    return render_template(
        "dashboard_form.html", dashboard=dashboard, perfis_vinculaveis=PERFIS_VINCULAVEIS
    )


@dashboards.route("/dashboards/<int:dashboard_id>/excluir", methods=["POST"])
@exige_perfil("admin")
def excluir(dashboard_id):
    db.session.delete(db.get_or_404(Dashboard, dashboard_id))
    db.session.commit()
    flash("Dashboard removido.", "success")
    return redirect(url_for("dashboards.listar"))
