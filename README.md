# Portal CPA — Faculdade Impacta

Portal web da **Comissão Própria de Avaliação (CPA)** da Faculdade Impacta. Ele centraliza, em um só lugar:

- **Transparência pública**: Mural de Devolutivas, Relatórios/Boletins em PDF e página de Contato, sem login.
- **Dashboards analíticos restritos**: painéis do Looker Studio (antigo Google Data Studio), exibidos por `<iframe>` conforme o perfil do usuário autenticado.
- **Painel administrativo**: a CPA gerencia dashboards, devolutivas, documentos e usuários sem alterar o código.

> **Status:** Fases 1 a 3 concluídas e todos os requisitos funcionais (RF01–RF09) implementados. Portal publicado na Vercel. Em andamento: revisão de acessibilidade (Fase 4), testes e validação (Fase 5), manual e treinamento (Fase 6).

---

## Sumário

1. [Visão geral](#visão-geral)
2. [Perfis e permissões](#perfis-e-permissões)
3. [Stack tecnológica](#stack-tecnológica)
4. [Arquitetura](#arquitetura)
5. [Estrutura do repositório](#estrutura-do-repositório)
6. [Banco de dados](#banco-de-dados)
7. [Segurança](#segurança)
8. [Configuração e execução](#configuração-e-execução)
9. [Requisitos](#requisitos)
10. [Roadmap](#roadmap)
11. [Contribuindo](#contribuindo)

---

## Visão geral

| Área | Quem acessa | O que faz |
|---|---|---|
| Página inicial | Todos | Apresentação institucional da CPA |
| Mural de Devolutivas | Todos (leitura) / Admin (gestão) | Demanda, área responsável, ação executada, status e data |
| Relatórios e Boletins | Todos (download) / Admin (upload) | PDFs organizados por ano e categoria |
| Contato | Todos | Informações da CPA e links para Google Chat e Google Meet |
| Dashboards | Usuários logados, por perfil | Painéis do Looker Studio incorporados |
| Gestão de usuários | Admin | Definir perfis e ativar ou desativar usuários |

### Dashboards

Relatórios oficiais da pesquisa da CPA no Looker Studio, separados por público respondente:

| Código | Relatório | Perfis |
|---|---|---|
| DASH-01 | Pesquisa CPA — Aluno(a) Presencial | Aluno, Coordenador, Avaliador MEC, Admin |
| DASH-02 | Pesquisa CPA — Aluno(a) EAD | Aluno, Coordenador, Avaliador MEC, Admin |
| DASH-03 | Pesquisa CPA — Professores | Coordenador, Avaliador MEC, Admin |
| DASH-04 | Pesquisa CPA — Corpo Técnico Administrativo | Coordenador, Avaliador MEC, Admin |

Os dados dos relatórios ainda são **fictícios**, com a mesma estrutura da pesquisa real. Eles só abrem para **contas Google da Impacta** logadas no navegador, e a permissão do Looker é independente do login do portal (detalhes em [Integração dos dashboards](docs/fase-3-desenvolvimento/03-integracao-dos-dashboards.md)).

### Documentos

| Código | Categoria | Formato |
|---|---|---|
| DOC-01 | Relatórios de Autoavaliação | PDF |
| DOC-02 | Boletins Informativos | PDF |

---

## Perfis e permissões

O **Visitante** não é um perfil cadastrado: é o usuário sem login (papel `anon`). Os outros quatro são linhas da tabela `perfis`.

| Funcionalidade | Visitante | Aluno | Coordenador | Avaliador MEC | Admin |
|---|:-:|:-:|:-:|:-:|:-:|
| Página inicial | ✅ | ✅ | ✅ | ✅ | ✅ |
| Mural de Devolutivas | Leitura | Leitura | Leitura | Leitura | Leitura + CRUD |
| Relatórios e Boletins | Baixar | Baixar | Baixar | Baixar | Baixar + Upload/Excluir |
| Contato | ✅ | ✅ | ✅ | ✅ | ✅ |
| DASH-01 Aluno(a) Presencial | ❌ | ✅ | ✅ | ✅ | ✅ + gerenciar link |
| DASH-02 Aluno(a) EAD | ❌ | ✅ | ✅ | ✅ | ✅ + gerenciar link |
| DASH-03 Professores | ❌ | ❌ | ✅ | ✅ | ✅ + gerenciar link |
| DASH-04 Corpo Técnico | ❌ | ❌ | ✅ | ✅ | ✅ + gerenciar link |
| Gestão de usuários | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Stack tecnológica

| Camada | Tecnologia | Papel |
|---|---|---|
| Front-end | **HTML5, CSS3, JavaScript** | Páginas responsivas renderizadas pelo Flask (templates Jinja2) |
| Back-end | **Python 3 + Flask** | Rotas, sessão, controle de acesso por perfil e painel administrativo |
| Banco de dados | **PostgreSQL (Supabase)** | Dados do portal, com Row Level Security |
| Autenticação | **Supabase Auth** | Login por e-mail e senha, hash bcrypt, emissão de JWT |
| Arquivos | **Supabase Storage** | Bucket `documentos`, somente PDF |
| Dashboards | **Looker Studio** | Painéis incorporados por `<iframe>` |
| Bibliotecas Python | `Flask-Login`, `Flask-SQLAlchemy`, `psycopg`, `supabase`, `python-dotenv` | Sessão, acesso ao banco, driver PostgreSQL, Auth do Supabase, leitura do `.env` |
| Versionamento | **Git + GitHub** | Código, migrations e documentação (RNF05) |

### Por que Supabase em vez de MySQL

A Fase 1 previa **Flask + MySQL** (RNF06). O Flask, o Python e o front em HTML/CSS/JS foram mantidos; **o MySQL foi substituído pelo PostgreSQL do Supabase**, porque ele já entrega pronto o que o projeto precisaria construir à mão:

| Necessidade (Fase 1) | Com MySQL | Com Supabase |
|---|---|---|
| Senha com hash (RNF02) | Implementar no Flask | Supabase Auth (bcrypt) |
| Consultas parametrizadas (RNF02) | Cuidar em cada query | API do Supabase já parametriza |
| Filtrar dashboards por perfil (RF02, RN02) | Só no Flask | No Flask **e** no banco (RLS) |
| Upload de PDF (RF08, RN04) | Salvar no servidor | Storage com filtro de tipo e tamanho |
| Hospedagem do banco | Configurar servidor | Gerenciada |

Os requisitos funcionais continuam valendo integralmente. Recomenda-se registrar a troca em ata e atualizar o texto do RNF06.

---

## Arquitetura

```
Navegador (HTML/CSS/JS)
        │  HTTP
        ▼
Flask (Python) ──────────────────────────────────┐
  • Flask-Login: sessão e @exige_perfil          │
  • área pública + área restrita por perfil      │
        │                    │                    │ <iframe>
        │ supabase-py        │ SQLAlchemy         ▼
        ▼                    ▼               Looker Studio
Supabase Auth          PostgreSQL (pooler)
  (login, contas)        + RLS + Storage
```

**Fluxo de login:**

1. O usuário envia e-mail e senha para o Flask.
2. O Flask valida as credenciais no **Supabase Auth** (`sign_in_with_password`); a senha nunca é gravada nas tabelas do portal.
3. Com o `id` devolvido, o Flask carrega o usuário em `public.usuarios`, confere se está ativo, abre a sessão (Flask-Login) e leva o usuário para `/dashboards`.
4. Cada rota restrita checa o perfil com o decorator `@exige_perfil` (`permissoes.py`). O admin tem acesso total; os demais perfis sem permissão recebem a página `403`. Visitante sem login é levado ao `/login`.

**Páginas e rotas:**

| Área | Rota | Quem acessa |
|---|---|---|
| Pública | `/` início, `/devolutivas`, `/relatorios`, `/contato`, `/login` | Todos, sem login (RN01) |
| Restrita | `/dashboards` | Logados; cada perfil vê só os painéis liberados |
| Restrita | `/aluno/avaliacoes` | Aluno |
| Restrita | `/coordenador` | Coordenador e admin |
| Restrita | `/admin` (usuários) | Admin |
| Gestão (admin) | Formulários nas próprias páginas de dashboards, devolutivas e relatórios | Admin |

**Quem protege o quê:**

| Acesso | Proteção |
|---|---|
| Páginas do Flask | `@exige_perfil` + `@login_required`. O Flask acessa o banco via SQLAlchemy com usuário de serviço (que ignora a RLS), então a regra de visibilidade dos dashboards é repetida em `Dashboard.visiveis_para()` |
| API do Supabase (chave pública) | **RLS** no banco, testada em `supabase/tests/` |
| Contas (criar, editar, excluir) | Supabase Auth Admin, com a `SUPABASE_SECRET_KEY`, só no servidor |

- `SUPABASE_PUBLISHABLE_KEY` — chave pública, usada no login. Respeita a RLS.
- `SUPABASE_SECRET_KEY` — chave secreta, **ignora a RLS**. Só no servidor, para gerenciar contas. Nunca vai para o navegador.

---

## Estrutura do repositório

```
cpa-developer/
├── README.md
├── LICENSE
├── SECURITY.md
├── .env.example            # modelo das variáveis de ambiente
├── .env                    # valores reais (NÃO versionado)
├── .gitignore
├── pyproject.toml          # metadados e regras do ruff
├── requirements.txt        # dependências Python
├── app.py                  # aplicação Flask: áreas do aluno, coordenador e admin; /saude
├── config.py               # configuração lida do .env (URL do banco, chaves)
├── models.py               # models SQLAlchemy mapeados às tabelas do Supabase
├── permissoes.py           # @exige_perfil (controle de acesso por perfil)
├── supabase_client.py      # clientes Supabase (público e admin)
├── routes/
│   ├── autenticacao.py     # login/logout via Supabase Auth
│   ├── publico.py          # início, mural, relatórios (upload PDF) e contato
│   └── dashboards.py       # dashboards por perfil e gestão dos links
├── templates/              # páginas HTML (Jinja2) sobre o layout comum (_layout.html)
├── static/css/base.css     # design system: cores, tipografia e componentes
├── scripts/
│   └── criar_usuarios_teste.py
├── .github/
│   ├── workflows/          # pr-checks.yml, codeql.yml
│   ├── dependabot.yml
│   └── pull_request_template.md
├── docs/
│   ├── README.md                 # índice da documentação
│   ├── plano-do-projeto.md       # 6 fases, 24 tarefas, progresso
│   ├── setup-supabase.md         # guia de configuração do Supabase
│   ├── fase-1-requisitos/        # ata, perfis, catálogo e requisitos
│   ├── fase-2-modelagem/         # banco, protótipos, navegação e validação
│   ├── fase-3-desenvolvimento/   # ambiente, autenticação, dashboards e página inicial
│   ├── fase-4-funcionalidades/   # mural, relatórios e contato
│   └── prints/                   # capturas de tela do portal
└── supabase/
    ├── config.toml
    ├── migrations/
    │   ├── 20261116000000_schema_inicial.sql
    │   ├── 20261116100000_corrige_leitura_dashboard_perfis.sql
    │   └── 20261117000000_avaliacoes_participacoes.sql
    ├── tests/
    │   └── rls_test.sql    # testes pgTAP das regras de acesso
    └── seed.sql
```

---

## Banco de dados

### Modelo

```
auth.users (Supabase Auth)
     │ 1:1  (trigger on_auth_user_created)
     ▼
usuarios ──N:1──► perfis
     │
     ├─ updated_by ──► dashboards ◄──N:M──► perfis   (via dashboard_perfis)
     ├─ created_by ──► devolutivas
     └─ created_by ──► documentos ──(storage_path)──► Storage: bucket "documentos"
```

| Tabela | Função |
|---|---|
| `perfis` | Domínio fixo: `aluno`, `coordenador`, `avaliador_mec`, `admin` |
| `usuarios` | Espelho de `auth.users` com nome, e-mail, perfil e `ativo`. **Sem coluna de senha** |
| `dashboards` | Código, nome, descrição, `url_embed`, `ativo`, `ordem` |
| `dashboard_perfis` | Quais perfis acessam cada dashboard (N:M) |
| `devolutivas` | Título, área responsável, ação, status (`planejado` / `em_andamento` / `concluido`), data |
| `documentos` | Metadados do PDF: título, descrição, categoria, ano, `storage_path` |

### Funções e triggers

| Item | O que faz |
|---|---|
| `perfil_atual()` | Código do perfil do usuário logado (ou `null` se inativo) |
| `is_admin()` | Atalho booleano usado nas policies |
| `set_updated_at()` | Atualiza `updated_at` em cada `UPDATE` |
| `handle_new_user()` | Todo novo cadastro no Auth vira **aluno** automaticamente |

### Regras de acesso (RLS)

| Tabela | Visitante | Usuário logado | Admin |
|---|---|---|---|
| `perfis` | — | leitura | — |
| `usuarios` | sem acesso | só a própria linha | lê e atualiza todas |
| `dashboards` | sem acesso | ativos do seu perfil; Avaliador MEC vê todos os ativos | tudo |
| `dashboard_perfis` | sem acesso | — | tudo |
| `devolutivas` | leitura | leitura | tudo |
| `documentos` | leitura | leitura | tudo |
| Storage `documentos` | leitura | leitura | upload, update, delete |

Admin e Avaliador MEC veem todos os dashboards **por regra na policy** (RN03), sem precisar de linhas em `dashboard_perfis`.

---

## Segurança

- **Sem escalada de privilégio no cadastro**: o perfil nunca vem dos dados enviados pelo cliente. Todo novo usuário é `aluno`; só um admin promove.
- **Sem auto-promoção**: não existe policy que permita ao usuário editar a própria linha em `usuarios`.
- **Usuário inativo** perde todas as permissões e a sessão aberta (é desconectado na próxima página).
- **Proteção CSRF**: todo formulário `POST` leva um token (Flask-WTF); envios sem token, vindos de outro site, são recusados.
- **Cookie de sessão** `HttpOnly`, `SameSite=Lax` e, em produção, só por HTTPS.
- **`url_embed` restrita** aos domínios `lookerstudio.google.com` e `datastudio.google.com`.
- **Storage**: somente `application/pdf`, até 20 MB (RN04). O navegador envia o PDF direto ao Storage com uma URL de uso único gerada pelo Flask (só para admin), sem passar pelo limite de ~4,5 MB da Vercel. O Flask confere a assinatura `%PDF` antes de cadastrar e apaga o arquivo se não for PDF.
- **Funções `security definer`** com `search_path = ''`.
- **Segredos fora do Git**: `.env` está no `.gitignore`. A `SUPABASE_SECRET_KEY` só existe no servidor.

---

## Configuração e execução

### Pré-requisitos

- Python 3.12+
- [Supabase CLI](https://supabase.com/docs/guides/cli) (para aplicar migrations)
- Acesso ao projeto Supabase

### 1. Variáveis de ambiente

```bash
cp .env.example .env
# preencha com os valores do Dashboard > Project Settings
```

| Variável | Uso |
|---|---|
| `SUPABASE_URL` | Endereço da API |
| `SUPABASE_PUBLISHABLE_KEY` | Chave pública (respeita RLS) |
| `SUPABASE_SECRET_KEY` | Chave secreta, só no backend |
| `SUPABASE_JWKS_URL` | Reservada para validar tokens JWT do Supabase |
| `SUPABASE_DB_HOST` / `PORT` / `NAME` / `USER` / `PASSWORD` | Conexão do Flask ao PostgreSQL (use o **pooler**, que funciona em IPv4) |
| `DATABASE_URL` | Opcional: URL completa do banco; substitui as `SUPABASE_DB_*` |
| `FLASK_SECRET_KEY` | Assinatura da sessão do Flask |
| `CPA_LINK_CHAT` / `CPA_LINK_MEET` / `CPA_EMAIL` | Opcionais: links da página de contato (sem eles, o portal usa os endereços gerais do Google e `cpa@faculdadeimpacta.edu.br`) |

> O host direto `db.<ref>.supabase.co` só tem IPv6. Em redes sem IPv6, use o pooler (Dashboard › **Connect**): host `aws-1-<regiao>.pooler.supabase.com`, usuário `postgres.<ref>`, porta `5432` (local) ou `6543` (serverless).

Detalhes da conexão e o que fazer se uma chave vazar: [docs/setup-supabase.md](docs/setup-supabase.md).

### 2. Aplicar o banco

```bash
supabase login
supabase link --project-ref <project-ref>
supabase db push                  # migrations, incluindo os dashboards oficiais
supabase migration list --remote  # confere o que foi aplicado
```

> Se aplicar uma migration pelo SQL Editor, registre-a depois com
> `supabase migration repair --status applied <versao> --remote`; sem isso, o deploy automático tenta aplicá-la de novo.

### 3. Rodar o Flask

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  |  source .venv/bin/activate (Linux/Mac)
pip install -r requirements.txt
flask run
```

Acesse `http://127.0.0.1:5000/saude`. A resposta `{"banco": "ok"}` confirma a conexão com o Supabase.

### 4. Usuários de teste

```bash
python -m scripts.criar_usuarios_teste             # cria as contas que faltam
python -m scripts.criar_usuarios_teste --redefinir # também troca a senha das existentes
```

| Perfil | E-mail |
|---|---|
| Aluno | `aluno@portal.com` |
| Coordenador | `coordenador@portal.com` |
| Avaliador MEC | `avaliador@portal.com` |
| Admin | `admin@portal.com` |

> O repositório é público, então as senhas **não** ficam no código: o script gera senhas aleatórias e as mostra uma única vez no terminal. Guarde-as fora do repositório. Novos usuários são criados pelo admin em `/admin`.

### Checklist de permissões

- Visitante lê `devolutivas` e `documentos`, mas **não** `dashboards`.
- Aluno vê só DASH-01 e DASH-02 (relatórios de alunos).
- Coordenador e Avaliador MEC veem os 4 dashboards.
- Aluno **não** consegue alterar `usuarios`.
- Upload de arquivo que não seja PDF é recusado.

---

## Requisitos

### Funcionais

| ID | Resumo | Situação |
|---|---|---|
| RF01 | Login com e-mail institucional e senha | ✅ Flask + Supabase Auth |
| RF02 | Controle de acesso por perfil (menus e URL direta) | ✅ `@exige_perfil` no Flask e RLS no banco |
| RF03 | Dashboards por perfil via iframe | ✅ `/dashboards`, filtrado por perfil |
| RF04 | Admin gerencia URLs dos dashboards | ✅ Cadastro, edição, ativação e perfis em `/dashboards` |
| RF05 | Mural público de devolutivas | ✅ `/devolutivas`, com filtro por status |
| RF06 | Admin gerencia devolutivas | ✅ Publicar, editar e excluir no próprio mural |
| RF07 | Lista pública de relatórios/boletins | ✅ `/relatorios`, com filtro por categoria e ano |
| RF08 | Admin faz upload de PDF | ✅ Upload para o Supabase Storage (só PDF, até 20 MB) |
| RF09 | Página de contato (Google Chat e Meet) | ✅ `/contato` (links configuráveis no `.env`) |

### Não funcionais

| ID | Requisito | Situação |
|---|---|---|
| RNF01 | Responsividade | ✅ Layout único; menu vira gaveta no celular e os iframes se ajustam à tela |
| RNF02 | Senhas com hash e consultas parametrizadas | Atendido por Supabase Auth e API |
| RNF03 | Usabilidade, contraste, seções públicas em até 2 cliques | ✅ Seções públicas a 1 clique pelo menu; validar contraste nos testes da Fase 5 |
| RNF04 | Chrome, Firefox, Edge e Safari | Testado no Chrome; demais navegadores na Fase 5 |
| RNF05 | Versionamento no GitHub | ✅ Repositório público |
| RNF06 | HTML/CSS/JS + Flask + banco relacional | Atualizado: MySQL → PostgreSQL (Supabase) |

### Regras de negócio

- **RN01** — Devolutivas, Relatórios/Boletins e Contato **nunca** exigem login.
- **RN02** — Os relatórios de Professores e Corpo Técnico Administrativo não podem ser listados nem acessados por alunos.
- **RN03** — Avaliador MEC tem leitura irrestrita dos dashboards ativos, sem edição.
- **RN04** — Apenas PDF é aceito na área de relatórios.

---

## Roadmap

Conforme o [Plano do projeto](docs/plano-do-projeto.md). Requisitos completos em [docs/](docs/README.md).

| Fase | Foco | Situação |
|---|---|---|
| 1 | Levantamento de requisitos | ✅ Concluída |
| 2 | Modelagem e design | ✅ Banco, protótipos, navegação e ajustes da validação documentados |
| 3 | Portal: ambiente, login, controle de acesso, dashboards, home | ✅ Concluída |
| 4 | Mural, relatórios, contato, acessibilidade | 🟡 Mural, relatórios e contato prontos e documentados; falta revisão de acessibilidade |
| 5 | Testes funcionais, de usabilidade e de segurança | ⏳ A fazer |
| 6 | Deploy, manual do usuário e treinamento | 🟡 Deploy na Vercel; faltam manual e treinamento |

### Próximos passos

1. Testar os 4 dashboards com uma conta Google da Impacta e atualizar as capturas de tela.
2. Revisão de acessibilidade (contraste, teclado, leitores de tela).
3. Testes automatizados das rotas Flask (`tests/`) e testes nos demais navegadores.
4. Manual do usuário e treinamento da CPA.

---

## Contribuindo

- Código e scripts de banco ficam no GitHub; evidências que não são código (atas, protótipos) ficam no Drive.
- Mudança de banco = **nova migration** em `supabase/migrations/` (`AAAAMMDDHHMMSS_descricao.sql`). Não edite migrations já aplicadas.
- Toda tabela nova precisa de **RLS habilitada** e policies explícitas.
- Nunca commite `.env`, senhas ou a `SUPABASE_SECRET_KEY`.

## Licença

Veja [LICENSE](LICENSE).
