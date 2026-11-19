# Plano do Projeto

Guia do que a equipe precisa desenvolver. Evidências que não são código vão para o **Drive**; o código vai para o **GitHub**.

**6 fases · 24 tarefas**

| Fase | Nome | Objetivo |
|:-:|---|---|
| 1 | [Levantamento de requisitos](#fase-1--levantamento-de-requisitos) | Entender necessidades, perfis, dashboards e conteúdos da CPA |
| 2 | [Modelagem e design](#fase-2--modelagem-e-design) | Arquitetura, banco de dados e protótipos |
| 3 | [Desenvolvimento do portal](#fase-3--desenvolvimento-do-portal) | Login, controle de acesso e dashboards |
| 4 | [Funcionalidades complementares](#fase-4--funcionalidades-complementares) | Mural, relatórios e contato |
| 5 | [Testes e validação](#fase-5--testes-e-validação) | Testes funcionais, de usabilidade e de segurança |
| 6 | [Implantação e treinamento](#fase-6--implantação-e-treinamento) | Deploy, manual e treinamento |

---

## Fase 1 — Levantamento de requisitos

Coletar informações detalhadas com a CPA sobre as necessidades, perfis de acesso, dashboards existentes e conteúdos a serem publicados.

- [x] Realizar reuniões com a CPA para entender os fluxos de trabalho e requisitos funcionais → [Ata](fase-1-requisitos/01-ata-reuniao.md)
- [x] Mapear os perfis de usuário e suas permissões de acesso → [Perfis e permissões](fase-1-requisitos/02-perfis-e-permissoes.md)
- [x] Identificar e catalogar os dashboards e documentos a serem integrados → [Catálogo](fase-1-requisitos/03-catalogo-dashboards-documentos.md)
- [x] Documentar os requisitos funcionais e não funcionais do portal → [Requisitos](fase-1-requisitos/04-requisitos.md)

## Fase 2 — Modelagem e design

Projetar a arquitetura do sistema, modelar o banco de dados e criar protótipos das telas para validação.

- [x] Modelar o banco de dados com tabelas para usuários, perfis e permissões → [Modelagem](fase-2-modelagem/01-modelagem-banco-de-dados.md)
- [x] Criar protótipos de interface para cada perfil de usuário → [Protótipos](fase-2-modelagem/02-prototipos-de-interface.md)
- [x] Definir a estrutura de navegação e layout responsivo → [Navegação](fase-2-modelagem/03-estrutura-de-navegacao.md)
- [x] Validar os protótipos com a CPA e ajustar conforme feedback → [Validação](fase-2-modelagem/04-validacao-dos-prototipos.md)

## Fase 3 — Desenvolvimento do portal

Implementar o portal web com sistema de login, controle de acesso e integração dos dashboards.

- [x] Configurar o ambiente de desenvolvimento e versionamento de código → [Ambiente](fase-3-desenvolvimento/01-configuracao-do-ambiente.md)
- [x] Desenvolver o sistema de autenticação e controle de acesso por perfil → [Autenticação](fase-3-desenvolvimento/02-autenticacao-e-controle-de-acesso.md)
- [x] Integrar os dashboards do Looker Studio nas páginas conforme permissões → [Dashboards](fase-3-desenvolvimento/03-integracao-dos-dashboards.md)
- [x] Criar a página inicial com dashboards dinâmicos e responsivos → [Página inicial](fase-3-desenvolvimento/04-pagina-inicial-e-dashboards.md)

## Fase 4 — Funcionalidades complementares

Desenvolver o mural de devolutivas, a área de relatórios e a página de contato.

- [x] Implementar o mural de devolutivas com área administrativa para publicação → [Mural](fase-4-funcionalidades/01-mural-de-devolutivas.md)
- [x] Criar a área de relatórios e boletins com upload e download de documentos → [Relatórios](fase-4-funcionalidades/02-relatorios-e-boletins.md)
- [x] Desenvolver a página de contato com links para Google Chat e Google Meet → [Contato](fase-4-funcionalidades/03-pagina-de-contato.md)
- [ ] Garantir que todas as páginas sejam responsivas e acessíveis

## Fase 5 — Testes e validação

Realizar testes funcionais, de usabilidade e de segurança com usuários reais para validar o portal.

- [ ] Executar testes de funcionalidade para cada perfil de usuário
- [ ] Realizar testes de usabilidade com alunos, coordenadores e avaliadores externos
- [ ] Corrigir bugs e ajustar a interface com base no feedback
- [ ] Validar a segurança do sistema de login e controle de acesso

## Fase 6 — Implantação e treinamento

Publicar o portal em produção, treinar os usuários e fornecer documentação técnica.

- [ ] Configurar o ambiente de produção e realizar o deploy do portal
- [ ] Criar manual do usuário e documentação técnica do código
- [ ] Realizar treinamentos com a CPA e demais usuários
- [ ] Acompanhar o uso inicial e coletar feedback para melhorias futuras
