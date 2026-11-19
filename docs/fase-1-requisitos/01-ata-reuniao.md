# Ata de Reunião e Alinhamento de Fluxos de Trabalho

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 1 — Levantamento de Requisitos
> **Data:** 12/11/2026

## Participantes

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

**Representação institucional:** Coordenação CPA / IPC (via escopo oficial)

---

## 1. Pauta da reunião

Compreensão dos processos atuais da CPA, mapeamento dos perfis de usuários e definição dos fluxos de publicação de dashboards, devolutivas e relatórios institucionais.

---

## 2. Fluxos de trabalho definidos

### 📊 Publicação de Dashboards

A CPA elabora os painéis analíticos no Google Data Studio (Looker Studio). O Administrador da CPA insere os links de incorporação diretamente pelo painel administrativo do portal, que libera a visualização conforme o perfil autenticado (Aluno, Coordenador ou Avaliador Externo MEC).

### 📌 Devolutivas Institucionais

Após o encerramento de cada ciclo de avaliação, a CPA registra no portal as demandas apontadas pela comunidade acadêmica e as ações corretivas executadas pelas áreas responsáveis. A consulta é aberta ao público, **sem necessidade de login**.

### 📄 Relatórios e Boletins

Documentos oficiais (em formato PDF) são enviados pelo Administrador da CPA e ficam disponíveis para download público, organizados por **ano** e **categoria**.

### 💬 Atendimento à Comunidade

O portal centraliza os links institucionais para contato direto com a CPA via **Google Chat** e **Google Meet**, respeitando os horários de atendimento da coordenação.

---

## 3. Deliberações e encaminhamentos

| Tema | Deliberação |
|---|---|
| **Arquitetura tecnológica** | Desenvolvimento em HTML5, CSS3, JavaScript, Python (Flask) e banco de dados relacional, garantindo gerenciamento dinâmico de conteúdo sem alteração no código-fonte. |
| **Links dos dashboards** | Como os links oficiais ainda serão disponibilizados pela CPA, o portal será desenvolvido e validado com **links de demonstração** do Looker Studio, com campo editável no painel administrativo para substituição imediata quando os endereços finais forem enviados. |

> **Atualização posterior:** o banco de dados definido inicialmente (MySQL) foi substituído pelo **PostgreSQL do Supabase**, mantendo Flask e o front-end em HTML/CSS/JS. Detalhes no [README](../../README.md#stack-tecnológica).
