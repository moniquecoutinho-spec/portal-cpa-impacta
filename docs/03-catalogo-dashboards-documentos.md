# Catálogo de Dashboards (Google Data Studio) e Documentos Institucionais
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 1 — Levantamento de Requisitos  
**Integrantes:**  Integrante 1: Monique Lima RA:2503159 Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307 Integrante 3: Alicya Sayuri Gallano Azato RA:2500140
**Data:** Novembro de 2026  

---

## 1. Dashboards Mapeados (Google Data Studio / Looker Studio)
Os painéis analíticos serão integrados ao portal via URL de incorporação (`<iframe>` responsivo), armazenada no banco de dados MySQL para permitir atualização direta pelo Administrador da CPA.

| Código | Nome do Dashboard | Conteúdo / Indicadores Principais | Perfis Autorizados | Status Atual |
| :--- | :--- | :--- | :--- | :--- |
| **DASH-01** | Pesquisa Institucional CPA | Satisfação geral, infraestrutura física, laboratórios, biblioteca e atendimento acadêmico. | Aluno, Coordenador, Avaliador MEC e Admin CPA | Mapeado (em ambiente de teste com link modelo) |
| **DASH-02** | Avaliação Docente por Curso | Indicadores de didática, cumprimento do plano de ensino e feedback dos docentes por curso. | Coordenador, Avaliador MEC e Admin CPA | Mapeado (em ambiente de teste com link modelo) |
| **DASH-03** | Acompanhamento de Egressos | Taxa de empregabilidade, área de atuação, faixa salarial e continuidade acadêmica dos ex-alunos. | Coordenador, Avaliador MEC e Admin CPA | Mapeado (em ambiente de teste com link modelo) |

## 2. Documentos Institucionais Mapeados (Área de Relatórios e Boletins)
Os documentos oficiais da CPA serão disponibilizados para consulta pública e download sem necessidade de login, organizados por categoria e ano de referência.

| Código | Categoria de Documento | Exemplos de Arquivos | Formato | Permissão de Leitura | Permissão de Envio/Exclusão |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **DOC-01** | Relatórios de Autoavaliação | Relatório Integral de Autoavaliação Institucional, Relatório Parcial de Ciclo Avaliativo | PDF (`.pdf`) | Público Geral (todos os perfis) | Exclusivo Administrador (CPA) |
| **DOC-02** | Boletins Informativos | Boletim Semestral de Resultados CPA, Informativo de Melhorias Institucionais | PDF (`.pdf`) | Público Geral (todos os perfis) | Exclusivo Administrador (CPA) |
