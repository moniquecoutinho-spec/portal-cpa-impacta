# Sistema de Autenticação e Controle de Acesso por Perfil (RBAC)

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 3 — Desenvolvimento do Portal

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

---

## 1. Fluxo de autenticação (`login.html` e rota `/login`)

O módulo de autenticação fica em `routes/autenticacao.py` e combina o **Supabase Auth** (validação da senha) com o **Flask-Login** (sessão do portal):

| Etapa | Funcionamento |
|---|---|
| **Validação de credenciais** | Ao enviar e-mail e senha, o Flask pede ao Supabase Auth a verificação. Se a senha confere, o portal busca o usuário na tabela `usuarios` (com o seu perfil) e confirma que o campo `ativo` está habilitado. |
| **Segurança de senhas** | Nenhuma senha fica em texto puro nem nas tabelas do portal: o Supabase Auth guarda apenas o hash bcrypt (RNF02). |
| **Criação de sessão** | Com a validação positiva, o Flask-Login grava o id do usuário em um cookie de sessão assinado com a chave secreta do Flask e redireciona para a área de dashboards. O nome e o perfil são lidos do banco a cada requisição, então uma troca de perfil vale na hora. |
| **Erro de login** | Credenciais inválidas ou conta desativada mostram o alerta "E-mail ou senha incorretos.", sem revelar qual dos dois falhou. |
| **Encerramento de sessão (`/logout`)** | Limpa a sessão ativa e devolve o usuário à página inicial pública. |

> **Atualização:** a primeira versão previa `flask.session` com `werkzeug.security` comparando a senha ao campo `senha_hash` do MySQL. Com a migração para o Supabase, a senha passou a ser validada pelo Supabase Auth, e a sessão do portal pelo Flask-Login.

---

## 2. Controle de acesso baseado em perfil (RBAC)

A proteção das rotas e funcionalidades segue **três camadas** simultâneas: back-end, interface e banco de dados.

| Camada de proteção | Regra implementada | Comportamento do sistema |
|---|---|---|
| **Bloqueio de rota restrita** | Decorador `@login_required` em `/dashboards` e nas áreas de perfil. | Visitante sem login é levado ao `/login` com o aviso "Faça login para acessar esta página." e volta à página pedida após entrar. |
| **Bloqueio por perfil** | Decorador `@exige_perfil(...)` (`permissoes.py`). | Perfil sem permissão recebe a tela "Acesso negado" (erro 403). O administrador passa em todas as verificações (acesso total). |
| **Filtragem de conteúdo** | `Dashboard.visiveis_para(perfil)` (`models.py`). | O aluno e o coordenador recebem só os dashboards ativos vinculados ao seu perfil em `dashboard_perfis`; o avaliador recebe todos os ativos; o admin recebe todos, inclusive os ocultos. |
| **Proteção de escrita (CRUD)** | `@exige_perfil("admin")` em todas as rotas `POST` de gestão. | Só o Administrador (CPA) cadastra, edita ou exclui dashboards, devolutivas, relatórios em PDF e usuários. |
| **Adaptação da interface** | Condicionais Jinja2 nos templates (`eh_admin`, `current_user.perfil`). | Formulários de gestão e botões de editar e excluir ficam ocultos para aluno, coordenador, avaliador e visitante. O menu mostra só as áreas do perfil. |
| **Proteção no banco** | *Row Level Security* (RLS) nas tabelas e no Storage. | Mesmo um acesso direto ao Supabase com a chave pública respeita as regras de perfil. Os testes em `supabase/tests/rls_test.sql` rodam a cada *pull request*. |

O Flask se conecta ao banco com o usuário de serviço, que não passa pelo RLS. Por isso a regra de visibilidade dos dashboards foi **replicada** em `Dashboard.visiveis_para()`, e o RLS segue protegendo qualquer acesso feito pela API do Supabase.

> **Atualização:** a filtragem previa as colunas `visivel_aluno`, `visivel_coordenador` e `visivel_avaliador`. Na versão adotada, os vínculos ficam na tabela `dashboard_perfis` (ver [modelagem do banco](../fase-2-modelagem/01-modelagem-banco-de-dados.md)).

---

## 3. Matriz de permissões por rota

| Rota | Visitante | Aluno | Coordenador | Avaliador MEC | Admin CPA |
|---|:---:|:---:|:---:|:---:|:---:|
| `/`, `/devolutivas`, `/relatorios`, `/contato` (leitura) | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/login` | ✅ | — | — | — | — |
| `/dashboards` (leitura, filtrada) | ❌ | ✅ | ✅ | ✅ | ✅ |
| `/aluno/avaliacoes` | ❌ | ✅ | ❌ | ❌ | ✅ |
| `/coordenador` (ciclos avaliativos) | ❌ | ❌ | ✅ | ❌ | ✅ |
| Gestão de dashboards, devolutivas, relatórios e `/admin` | ❌ | ❌ | ❌ | ❌ | ✅ |
