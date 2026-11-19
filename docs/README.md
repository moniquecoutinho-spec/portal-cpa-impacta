# Documentação do Portal CPA

| Documento | Conteúdo |
|---|---|
| [Plano do projeto](plano-do-projeto.md) | 6 fases, 24 tarefas e o progresso de cada uma |
| [Configuração do Supabase](setup-supabase.md) | Variáveis de ambiente, conexão, migrations e o que fazer se uma chave vazar |

## Fase 1 — Levantamento de requisitos

| # | Documento | Conteúdo |
|:-:|---|---|
| 01 | [Ata de reunião](fase-1-requisitos/01-ata-reuniao.md) | Fluxos de trabalho e deliberações com a CPA |
| 02 | [Perfis e permissões](fase-1-requisitos/02-perfis-e-permissoes.md) | Perfis de acesso e matriz de permissões |
| 03 | [Catálogo de dashboards e documentos](fase-1-requisitos/03-catalogo-dashboards-documentos.md) | Dashboards oficiais (DASH-01 a 04) e documentos (DOC-01 a 02) |
| 04 | [Requisitos](fase-1-requisitos/04-requisitos.md) | RF01–RF09, RNF01–RNF06 e RN01–RN04 |

## Fase 2 — Modelagem e design

| # | Documento | Conteúdo |
|:-:|---|---|
| 01 | [Modelagem do banco de dados](fase-2-modelagem/01-modelagem-banco-de-dados.md) | Diagrama ER, dicionário de dados e mudanças da versão MySQL para o Supabase |
| 02 | [Protótipos de interface](fase-2-modelagem/02-prototipos-de-interface.md) | Telas de cada perfil, com capturas do portal |
| 03 | [Estrutura de navegação](fase-2-modelagem/03-estrutura-de-navegacao.md) | Mapa de páginas, menu e layout responsivo |
| 04 | [Validação dos protótipos](fase-2-modelagem/04-validacao-dos-prototipos.md) | Aspectos validados e ajustes incorporados |

## Fase 3 — Desenvolvimento do portal

| # | Documento | Conteúdo |
|:-:|---|---|
| 01 | [Configuração do ambiente](fase-3-desenvolvimento/01-configuracao-do-ambiente.md) | Stack, estrutura do repositório e fluxo no GitHub |
| 02 | [Autenticação e controle de acesso](fase-3-desenvolvimento/02-autenticacao-e-controle-de-acesso.md) | Login, sessão e as três camadas do RBAC |
| 03 | [Integração dos dashboards](fase-3-desenvolvimento/03-integracao-dos-dashboards.md) | Incorporação do Looker Studio, matriz por perfil e gestão dos links |
| 04 | [Página inicial e dashboards](fase-3-desenvolvimento/04-pagina-inicial-e-dashboards.md) | Página inicial pública e exibição responsiva dos painéis |

## Fase 4 — Funcionalidades complementares

| # | Documento | Conteúdo |
|:-:|---|---|
| 01 | [Mural de devolutivas](fase-4-funcionalidades/01-mural-de-devolutivas.md) | Página pública e publicação pelo admin |
| 02 | [Relatórios e boletins](fase-4-funcionalidades/02-relatorios-e-boletins.md) | Repositório de PDFs, filtros e upload direto ao Storage |
| 03 | [Página de contato](fase-4-funcionalidades/03-pagina-de-contato.md) | Google Chat, Google Meet e e-mail configuráveis |
| 04 | Acessibilidade | *A fazer* |
