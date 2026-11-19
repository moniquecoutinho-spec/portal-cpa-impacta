"""Models mapeados para as tabelas do Supabase (criadas pelas migrations).

As tabelas NÃO são criadas pelo SQLAlchemy (sem db.create_all()): a fonte da
verdade do schema são os arquivos em supabase/migrations/.
"""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

# Código usado pelas rotas/templates  ->  código gravado no banco
PERFIL_APP_PARA_BANCO = {
    "aluno": "aluno",
    "coordenador": "coordenador",
    "avaliador": "avaliador_mec",
    "admin": "admin",
}
PERFIL_BANCO_PARA_APP = {banco: app for app, banco in PERFIL_APP_PARA_BANCO.items()}
PERFIS_VALIDOS = list(PERFIL_APP_PARA_BANCO)


class Perfil(db.Model):
    __tablename__ = "perfis"

    id = db.Column(db.SmallInteger, primary_key=True)
    codigo = db.Column(db.Text, unique=True, nullable=False)
    nome = db.Column(db.Text, nullable=False)

    @classmethod
    def por_codigo_app(cls, codigo_app: str) -> "Perfil":
        return cls.query.filter_by(codigo=PERFIL_APP_PARA_BANCO[codigo_app]).one()


class Usuario(db.Model, UserMixin):
    """Espelho de auth.users. A senha fica no Supabase Auth, não aqui."""

    __tablename__ = "usuarios"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    perfil_id = db.Column(db.SmallInteger, db.ForeignKey("perfis.id"), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, server_default=db.true())

    perfil_rel = db.relationship(Perfil, lazy="joined")

    @property
    def perfil(self) -> str:
        """Código do perfil no formato usado pelo app ('avaliador', não 'avaliador_mec')."""
        return PERFIL_BANCO_PARA_APP[self.perfil_rel.codigo]

    @property
    def is_active(self) -> bool:
        return self.ativo

    @classmethod
    def query_por_perfil(cls, codigo_app: str):
        return cls.query.join(Perfil).filter(Perfil.codigo == PERFIL_APP_PARA_BANCO[codigo_app])


dashboard_perfis = db.Table(
    "dashboard_perfis",
    db.Column("dashboard_id", db.BigInteger, db.ForeignKey("dashboards.id"), primary_key=True),
    db.Column("perfil_id", db.SmallInteger, db.ForeignKey("perfis.id"), primary_key=True),
)


class Dashboard(db.Model):
    """Painel do Looker Studio (Google Data Studio) incorporado por iframe."""

    __tablename__ = "dashboards"

    id = db.Column(db.BigInteger, primary_key=True)
    codigo = db.Column(db.Text, unique=True, nullable=False)
    nome = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text)
    url_embed = db.Column(db.Text, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, server_default=db.true())
    ordem = db.Column(db.SmallInteger, nullable=False, server_default="0")
    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"))

    perfis = db.relationship(Perfil, secondary=dashboard_perfis, lazy="selectin")

    @property
    def perfis_app(self) -> set[str]:
        """Perfis vinculados, no formato do app ('aluno', 'coordenador')."""
        return {PERFIL_BANCO_PARA_APP[p.codigo] for p in self.perfis}

    @classmethod
    def visiveis_para(cls, perfil_app: str):
        """Regra da RLS replicada no Flask (o app conecta como postgres e ignora a RLS).

        Admin vê todos (inclusive inativos, para gerenciar). Avaliador MEC vê
        todos os ativos (RN03). Os demais veem os ativos vinculados ao perfil.
        """
        consulta = cls.query.order_by(cls.ordem, cls.id)
        if perfil_app == "admin":
            return consulta
        consulta = consulta.filter(cls.ativo.is_(True))
        if perfil_app == "avaliador":
            return consulta
        return consulta.filter(cls.perfis.any(Perfil.codigo == PERFIL_APP_PARA_BANCO[perfil_app]))


STATUS_DEVOLUTIVA = {
    "planejado": "Planejado",
    "em_andamento": "Em andamento",
    "concluido": "Concluído",
}


class Devolutiva(db.Model):
    """Mural público: resposta da instituição a uma demanda da avaliação."""

    __tablename__ = "devolutivas"

    id = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    area_responsavel = db.Column(db.Text, nullable=False)
    acao = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False, server_default="planejado")
    data_publicacao = db.Column(db.Date, nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"))

    @property
    def status_rotulo(self) -> str:
        return STATUS_DEVOLUTIVA.get(self.status, self.status)


CATEGORIAS_DOCUMENTO = {
    "relatorio_autoavaliacao": "Relatório de Autoavaliação",
    "boletim_informativo": "Boletim Informativo",
}


class Documento(db.Model):
    """Relatório ou boletim em PDF; o arquivo fica no bucket 'documentos' do Storage."""

    __tablename__ = "documentos"

    id = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.Text, nullable=False)
    ano_referencia = db.Column(db.SmallInteger, nullable=False)
    storage_path = db.Column(db.Text, unique=True, nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"))

    @property
    def categoria_rotulo(self) -> str:
        return CATEGORIAS_DOCUMENTO.get(self.categoria, self.categoria)


class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"

    id = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    status = db.Column(db.Text, nullable=False, server_default="Agendada")


class Participacao(db.Model):
    __tablename__ = "participacoes"

    id = db.Column(db.BigInteger, primary_key=True)
    aluno_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False)
    avaliacao_id = db.Column(db.BigInteger, db.ForeignKey("avaliacoes.id"), nullable=False)
    respondida = db.Column(db.Boolean, nullable=False, server_default=db.false())
