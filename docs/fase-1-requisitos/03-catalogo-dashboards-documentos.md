# Catálogo de Dashboards e Documentos Institucionais

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 1 — Levantamento de Requisitos
> **Data:** Novembro de 2026

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

---

## 1. Dashboards mapeados (Looker Studio)

Os painéis analíticos são integrados ao portal via **URL de incorporação** (`<iframe>` responsivo), armazenada no banco de dados para permitir atualização direta pelo Administrador da CPA.

| Código | Dashboard | Indicadores principais | Perfis autorizados | Status |
|---|---|---|---|---|
| `DASH-01` | **Pesquisa Institucional CPA** | Satisfação geral, infraestrutura física, laboratórios, biblioteca e atendimento acadêmico | Aluno, Coordenador, Avaliador MEC, Admin CPA | 🟡 Mapeado (link de teste) |
| `DASH-02` | **Avaliação Docente por Curso** | Didática, cumprimento do plano de ensino e feedback dos docentes por curso | Coordenador, Avaliador MEC, Admin CPA | 🟡 Mapeado (link de teste) |
| `DASH-03` | **Acompanhamento de Egressos** | Empregabilidade, área de atuação, faixa salarial e continuidade acadêmica dos ex-alunos | Coordenador, Avaliador MEC, Admin CPA | 🟡 Mapeado (link de teste) |

> Os links de teste são substituídos pelo Admin no painel quando a CPA enviar os endereços oficiais.

---

## 2. Documentos institucionais (Relatórios e Boletins)

Os documentos oficiais da CPA ficam disponíveis para consulta pública e download, **sem necessidade de login**, organizados por categoria e ano de referência.

| Código | Categoria | Exemplos de arquivos | Formato | Leitura | Envio / exclusão |
|---|---|---|---|---|---|
| `DOC-01` | **Relatórios de Autoavaliação** | Relatório Integral de Autoavaliação Institucional; Relatório Parcial de Ciclo Avaliativo | PDF | Público geral | Exclusivo Admin CPA |
| `DOC-02` | **Boletins Informativos** | Boletim Semestral de Resultados CPA; Informativo de Melhorias Institucionais | PDF | Público geral | Exclusivo Admin CPA |
