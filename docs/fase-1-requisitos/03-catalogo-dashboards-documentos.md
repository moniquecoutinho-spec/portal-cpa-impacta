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
>
> **Atualização (19/11/2026):** a CPA enviou os relatórios oficiais de incorporação. Em vez dos 3 painéis temáticos acima, a pesquisa é dividida em **4 relatórios por público respondente**, já cadastrados no portal (migration `20261119000000_dashboards_oficiais.sql`):
>
> | Código | Relatório | Público respondente | Perfis autorizados |
> |---|---|---|---|
> | `DASH-01` | **Pesquisa CPA — Aluno(a) Presencial** | Alunos dos cursos presenciais | Aluno, Coordenador, Avaliador MEC, Admin CPA |
> | `DASH-02` | **Pesquisa CPA — Aluno(a) EAD** | Alunos dos cursos a distância | Aluno, Coordenador, Avaliador MEC, Admin CPA |
> | `DASH-03` | **Pesquisa CPA — Professores** | Corpo docente | Coordenador, Avaliador MEC, Admin CPA |
> | `DASH-04` | **Pesquisa CPA — Corpo Técnico Administrativo** | Colaboradores técnico-administrativos | Coordenador, Avaliador MEC, Admin CPA |
>
> A regra RN02 continua valendo: os relatórios de professores e do corpo técnico não são listados para alunos.
>
> **Limitações conhecidas, apontadas pela CPA:**
>
> - Os relatórios só abrem para **contas Google do domínio Impacta** logadas no navegador. Com conta pessoal, o painel mostra "acesso negado"; o portal avisa isso acima dos dashboards.
> - O login do portal e a permissão do Looker Studio são **independentes**: qualquer pessoa do domínio com o link abre o relatório fora do portal. O portal organiza o que cada perfil vê; o sigilo real depende do compartilhamento no Looker, que a CPA fará na versão definitiva (por exemplo, relatórios restritos a coordenadores).
> - O **Avaliador Externo (MEC)** não tem conta Impacta. A CPA vai definir uma solução específica, como compartilhamento individual ou versão pública com dados agregados.
> - Os dados atuais dos relatórios são **fictícios**, com a mesma estrutura da pesquisa real; a troca para a base oficial não muda os links.

---

## 2. Documentos institucionais (Relatórios e Boletins)

Os documentos oficiais da CPA ficam disponíveis para consulta pública e download, **sem necessidade de login**, organizados por categoria e ano de referência.

| Código | Categoria | Exemplos de arquivos | Formato | Leitura | Envio / exclusão |
|---|---|---|---|---|---|
| `DOC-01` | **Relatórios de Autoavaliação** | Relatório Integral de Autoavaliação Institucional; Relatório Parcial de Ciclo Avaliativo | PDF | Público geral | Exclusivo Admin CPA |
| `DOC-02` | **Boletins Informativos** | Boletim Semestral de Resultados CPA; Informativo de Melhorias Institucionais | PDF | Público geral | Exclusivo Admin CPA |
