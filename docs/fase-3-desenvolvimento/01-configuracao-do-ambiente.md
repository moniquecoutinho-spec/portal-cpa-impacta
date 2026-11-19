# Configuração do Ambiente de Desenvolvimento e Versionamento de Código

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 3 — Desenvolvimento do Portal

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

---

## 1. Ambiente técnico padronizado

Para o desenvolvimento integrado entre front-end, back-end e banco de dados, a equipe padronizou o seguinte ambiente:

| Camada / ferramenta | Tecnologia adotada | Finalidade no projeto |
|---|---|---|
| **Back-end** | Python 3.12+ com Flask 3 | Rotas, sessões de login, regras de perfil e upload de arquivos. |
| **Sessão e login** | Flask-Login | Mantém o usuário autenticado e protege as rotas restritas. |
| **Banco de dados** | PostgreSQL do **Supabase** | Armazenamento relacional de usuários, perfis, dashboards, devolutivas, documentos e ciclos avaliativos. |
| **Acesso ao banco** | Flask-SQLAlchemy + psycopg 3 | Consultas parametrizadas pelo ORM, via *pooler* do Supabase. |
| **Autenticação e arquivos** | Supabase Auth e Supabase Storage (SDK `supabase`) | Validação de e-mail e senha; armazenamento dos PDFs no bucket `documentos`. |
| **Front-end** | HTML5, CSS3 e JavaScript | Telas responsivas renderizadas pelo motor de templates Jinja2. |
| **Versionamento** | Git e GitHub | Histórico, integração das entregas da equipe e hospedagem do código. |
| **Hospedagem** | Vercel | Publicação do portal a partir da branch `main`. |

> **Atualização:** a primeira versão deste documento previa MySQL/MariaDB (banco `portal_cpa`) com o conector `mysql-connector-python`. O projeto migrou para o **Supabase**, que entrega em um só serviço o PostgreSQL, a autenticação, o armazenamento de arquivos e as regras de acesso no banco (RLS). As dependências estão em `requirements.txt` e `pyproject.toml`.

---

## 2. Estrutura de diretórios do repositório (`cpa-developer`)

| Caminho | Conteúdo |
|---|---|
| `docs/` | Documentação técnica e funcional por fase (`fase-1-requisitos/`, `fase-2-modelagem/`, `fase-3-desenvolvimento/`, `fase-4-funcionalidades/`…) e capturas de tela (`prints/`). |
| `supabase/` | Migrations SQL (criação das tabelas e regras de acesso), `seed.sql` (carga inicial) e testes de RLS. |
| `templates/` | Páginas HTML dinâmicas (`index.html`, `login.html`, `dashboards.html`, `devolutivas.html`, `relatorios.html`, `contato.html` e as áreas de cada perfil). |
| `static/` | Estilos (`css/base.css`), scripts e imagens. Os PDFs **não** ficam aqui: vão para o Supabase Storage. |
| `routes/` | Blueprints do Flask: `autenticacao.py`, `publico.py` (área pública) e `dashboards.py`. |
| `app.py` | Aplicação principal: configuração, áreas por perfil e tratamento de erros. |
| `models.py`, `permissoes.py`, `config.py` | Tabelas mapeadas, decorador de controle de acesso e leitura das variáveis de ambiente. |
| `scripts/` | Utilitários, como a criação dos usuários de teste. |
| `requirements.txt` | Dependências para reproduzir o ambiente. |

> **Atualização:** o script único `sql/banco_cpa.sql` foi substituído por **migrations versionadas** em `supabase/migrations/`, aplicadas em ordem. O diretório `static/uploads/` deu lugar ao Supabase Storage, porque a hospedagem na Vercel não mantém arquivos gravados no servidor.

Credenciais (chaves do Supabase, senha do banco, chave de sessão do Flask) ficam no arquivo `.env`, que **não é versionado**. O modelo com os nomes das variáveis está em `.env.example`.

---

## 3. Fluxo de versionamento e colaboração no GitHub

| Prática | Como foi aplicada |
|---|---|
| **Repositório público** | [`4Diovanni/cpa-developer`](https://github.com/4Diovanni/cpa-developer), com acesso de colaboração para os integrantes (RNF05). |
| **Branches por entrega** | Nada é feito direto na `main`. Cada mudança nasce em uma branch `<tipo>/<descricao>` (ex.: `feat/area-publica-e-dashboards`) e entra por *pull request*. |
| **Commits padronizados** | Padrão *Conventional Commits* (`feat`, `fix`, `docs`, `refactor`…), com mensagens descritivas em português. |
| **Verificação automática (CI)** | A cada *pull request*, o GitHub Actions confere o padrão do título e da branch, procura segredos expostos (Gitleaks), valida o Markdown e os links, aplica as migrations em um Postgres limpo, roda os testes de RLS e faz o lint do Python (ruff) e a auditoria das dependências. |
| **Segurança contínua** | CodeQL analisa o código e o Dependabot abre atualizações semanais das dependências. |
| **Banco sincronizado** | A integração do Supabase com o GitHub aplica as migrations novas no banco de produção quando o *pull request* é aceito. |
| **Publicação** | A Vercel publica a versão da `main` automaticamente. |
