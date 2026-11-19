# Modelagem do Banco de Dados (MER e Dicionário de Dados)

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 2 — Modelagem e Design
> **SGBD:** PostgreSQL (Supabase) · schema `public`

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

---

## 1. Arquitetura relacional e regras de integridade

O banco foi estruturado para isolar as permissões por perfil e permitir que a CPA atualize os conteúdos **sem alterar o código-fonte**.

| Regra | Como foi modelada |
|---|---|
| **Relacionamento 1:N (perfis → usuarios)** | Cada perfil pode ter vários usuários; cada usuário tem obrigatoriamente um único perfil, pela chave estrangeira `perfil_id`. |
| **Controle de visibilidade (dashboards)** | A tabela associativa `dashboard_perfis` (N:N) indica quais perfis veem cada painel. Admin e Avaliador MEC veem todos os painéis ativos por regra (RN03), sem precisar de vínculo. |
| **Transparência pública (devolutivas e documentos)** | Leitura liberada a qualquer visitante, sem login (RN01); escrita exclusiva do perfil Administrador (CPA). |
| **Senhas fora das tabelas do portal** | A autenticação fica no **Supabase Auth** (`auth.users`, hash bcrypt). A tabela `usuarios` guarda só os dados do portal (RNF02). |
| **Proteção no próprio banco** | Todas as tabelas têm **Row Level Security (RLS)** com policies por perfil, testadas automaticamente (`supabase/tests/rls_test.sql`). |

> **Atualização da modelagem:** a primeira versão deste documento previa MySQL/MariaDB (banco `portal_cpa`). O projeto adotou o **PostgreSQL do Supabase**, o que trouxe as mudanças abaixo. A finalidade de cada tabela foi mantida.
>
> | Versão MySQL | Versão adotada (Supabase) | Motivo |
> |---|---|---|
> | `usuarios.senha_hash` | Senha no Supabase Auth | Hash e sessão gerenciados pelo serviço de autenticação |
> | `usuarios.id INT` | `usuarios.id uuid` (mesmo id do `auth.users`) | Vínculo direto com a conta do Auth |
> | `usuarios.matricula` | Não adotado | Nenhum fluxo do portal usa o RA |
> | `dashboards.visivel_aluno / _coordenador / _avaliador` | Tabela `dashboard_perfis` | Permite novos perfis sem nova coluna; avaliador vê tudo por regra |
> | Tabela `relatorios` (`arquivo_nome` no servidor) | Tabela `documentos` (`storage_path` no Supabase Storage) | Arquivo em bucket público só de PDF |
> | `relatorios.tipo` com a opção "Outro" | `documentos.categoria` com 2 valores | Segue o catálogo da Fase 1 (DOC-01 e DOC-02) |
> | `devolutivas.demanda_identificada` + `acao_realizada` | `devolutivas.titulo` (a demanda) + `acao` | Mesmo conteúdo, nomes mais curtos |

---

## 2. Diagrama entidade-relacionamento

```mermaid
erDiagram
    perfis ||--o{ usuarios : "define o acesso de"
    perfis ||--o{ dashboard_perfis : ""
    dashboards ||--o{ dashboard_perfis : "liberado para"
    usuarios ||--o{ devolutivas : "publica (admin)"
    usuarios ||--o{ documentos : "envia (admin)"
    usuarios ||--o{ participacoes : "responde (aluno)"
    avaliacoes ||--o{ participacoes : ""

    perfis { smallint id PK; text codigo UK; text nome }
    usuarios { uuid id PK; text nome; text email UK; smallint perfil_id FK; boolean ativo }
    dashboards { bigint id PK; text codigo UK; text nome; text url_embed; boolean ativo; smallint ordem }
    dashboard_perfis { bigint dashboard_id PK; smallint perfil_id PK }
    devolutivas { bigint id PK; text titulo; text area_responsavel; text acao; text status; date data_publicacao }
    documentos { bigint id PK; text titulo; text categoria; smallint ano_referencia; text storage_path UK }
    avaliacoes { bigint id PK; text titulo; date data_inicio; date data_fim; text status }
    participacoes { bigint id PK; uuid aluno_id FK; bigint avaliacao_id FK; boolean respondida }
```

---

## 3. Dicionário de dados

### Tabela 1: `perfis` (níveis de acesso)

| Campo | Tipo | Restrição / chave | Descrição |
|---|---|---|---|
| `id` | `smallint` | PK, identity | Identificador do perfil. |
| `codigo` | `text` | UNIQUE, NOT NULL, CHECK | `aluno`, `coordenador`, `avaliador_mec` ou `admin`. Usado nas regras de acesso. |
| `nome` | `text` | NOT NULL | Nome de exibição (ex.: "Coordenador de Curso"). |
| `descricao` | `text` | NULL | Resumo das permissões do perfil. |

> O **Visitante** não é uma linha desta tabela: é quem acessa sem login (papel `anon` do Supabase).

### Tabela 2: `usuarios` (cadastro)

| Campo | Tipo | Restrição / chave | Descrição |
|---|---|---|---|
| `id` | `uuid` | PK, FK → `auth.users.id` (cascade) | Mesmo id da conta no Supabase Auth. |
| `nome` | `text` | NOT NULL | Nome completo do usuário. |
| `email` | `text` | UNIQUE, NOT NULL | E-mail institucional usado no login. |
| `perfil_id` | `smallint` | FK → `perfis.id`, NOT NULL | Nível de acesso no portal. |
| `ativo` | `boolean` | DEFAULT `true` | Conta ativa (`true`) ou bloqueada (`false`). Conta inativa não faz login. |
| `created_at` / `updated_at` | `timestamptz` | DEFAULT `now()` | Datas de criação e última alteração. |

> Toda conta nova entra como **aluno** (trigger `handle_new_user`). Só um admin promove a outro perfil, o que impede a autopromoção.

### Tabela 3: `dashboards` (painéis do Looker Studio / Google Data Studio)

| Campo | Tipo | Restrição / chave | Descrição |
|---|---|---|---|
| `id` | `bigint` | PK, identity | Identificador do dashboard. |
| `codigo` | `text` | UNIQUE, NOT NULL | Código do catálogo (`DASH-01`, `DASH-02`…). |
| `nome` | `text` | NOT NULL | Nome de exibição do painel. |
| `descricao` | `text` | NULL | Resumo dos indicadores. |
| `url_embed` | `text` | NOT NULL, CHECK de domínio | Link de incorporação (iframe). Só aceita `lookerstudio.google.com` ou `datastudio.google.com`. |
| `ativo` | `boolean` | DEFAULT `true` | Painel visível (`true`) ou oculto (`false`) para os perfis. |
| `ordem` | `smallint` | DEFAULT `0` | Ordem de exibição na página. |
| `updated_by` | `uuid` | FK → `usuarios.id` | Admin que alterou por último. |
| `created_at` / `updated_at` | `timestamptz` | DEFAULT `now()` | Datas de criação e última troca do link. |

### Tabela 4: `dashboard_perfis` (quem vê cada dashboard)

| Campo | Tipo | Restrição / chave | Descrição |
|---|---|---|---|
| `dashboard_id` | `bigint` | PK, FK → `dashboards.id` (cascade) | Dashboard liberado. |
| `perfil_id` | `smallint` | PK, FK → `perfis.id` (cascade) | Perfil que pode ver o dashboard. |

### Tabela 5: `devolutivas` (mural público de transparência)

| Campo | Tipo | Restrição / chave | Descrição |
|---|---|---|---|
| `id` | `bigint` | PK, identity | Identificador da devolutiva. |
| `titulo` | `text` | NOT NULL | Demanda identificada na pesquisa da CPA. |
| `area_responsavel` | `text` | NOT NULL | Setor responsável (ex.: TI, Biblioteca). |
| `acao` | `text` | NOT NULL | Providência adotada pela instituição. |
| `status` | `text` | CHECK, DEFAULT `planejado` | `planejado`, `em_andamento` ou `concluido`. |
| `data_publicacao` | `date` | NOT NULL, DEFAULT hoje | Data de publicação no mural. |
| `created_by` | `uuid` | FK → `usuarios.id` | Admin que publicou. |

### Tabela 6: `documentos` (relatórios e boletins em PDF)

| Campo | Tipo | Restrição / chave | Descrição |
|---|---|---|---|
| `id` | `bigint` | PK, identity | Identificador do documento. |
| `titulo` | `text` | NOT NULL | Título oficial do relatório ou boletim. |
| `descricao` | `text` | NULL | Resumo do conteúdo. |
| `categoria` | `text` | CHECK | `relatorio_autoavaliacao` (DOC-01) ou `boletim_informativo` (DOC-02). |
| `ano_referencia` | `smallint` | NOT NULL, entre 2000 e 2100 | Ano-base do documento. |
| `storage_path` | `text` | UNIQUE, termina em `.pdf` | Caminho do arquivo no bucket `documentos` do Supabase Storage. |
| `created_by` | `uuid` | FK → `usuarios.id` | Admin que enviou. |

> O bucket `documentos` é público para leitura e só aceita `application/pdf` com até 20 MB (RN04).
>
> **Envio na hospedagem:** a Vercel aceita no máximo cerca de **4,5 MB** por requisição. Por isso o navegador do admin envia o PDF **direto ao Storage**, com uma URL de uso único gerada pelo Flask, e o limite efetivo passa a ser o do bucket (20 MB).

### Tabelas 7 e 8: `avaliacoes` e `participacoes` (ciclos avaliativos)

Usadas pela área do coordenador (cadastro dos ciclos) e pela área do aluno (consulta dos ciclos).

| Tabela | Campos principais | Descrição |
|---|---|---|
| `avaliacoes` | `titulo`, `data_inicio`, `data_fim` (≥ início), `status` | Ciclo de avaliação institucional e seu período de respostas. |
| `participacoes` | `aluno_id` → `usuarios`, `avaliacao_id` → `avaliacoes`, `respondida` | Participação de cada aluno em cada ciclo (um registro por par aluno/ciclo). Base do indicador de participação. |

---

## 4. Implementação

| Arquivo | Conteúdo |
|---|---|
| `supabase/migrations/20261116000000_schema_inicial.sql` | Tabelas, funções `perfil_atual()` e `is_admin()`, triggers, RLS e bucket de PDFs |
| `supabase/migrations/20261116100000_corrige_leitura_dashboard_perfis.sql` | Permite ao aluno e ao coordenador lerem os próprios vínculos |
| `supabase/migrations/20261117000000_avaliacoes_participacoes.sql` | Tabelas de ciclos avaliativos e participação |
| `supabase/migrations/20261119000000_dashboards_oficiais.sql` | Os 4 dashboards oficiais da CPA (DASH-01 a 04) e os vínculos com perfis |
| `supabase/seed.sql` | Carga inicial do banco local (os dashboards ficam na migration acima) |
| `supabase/tests/rls_test.sql` | Testes automáticos das regras de acesso (pgTAP) |
