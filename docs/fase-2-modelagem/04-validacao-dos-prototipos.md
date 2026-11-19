# Registro de Validação dos Protótipos e Ajustes de Design

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 2 — Modelagem e Design

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

---

## 1. Objetivo e escopo da validação

Avaliar os protótipos de tela em HTML/CSS e a estrutura do banco de dados frente aos requisitos da Fase 1, garantindo que todos os perfis tenham seus fluxos atendidos de forma clara e intuitiva antes da integração final com o back-end em Python (Flask).

---

## 2. Aspectos validados

| Aspecto | Resultado |
|---|---|
| **Transparência pública** | Confirmado que o mural de devolutivas, os relatórios em PDF e a página de contato funcionam **sem login**, atendendo às normas de publicidade institucional (RN01). |
| **Identificação do perfil** | Aprovada a exibição do nome e do perfil ativo no menu após o login, orientando o usuário sobre o seu nível de acesso. |
| **Canais de atendimento** | Validada a disposição dos botões diretos para Google Chat e Google Meet na página de contato. |
| **Isolamento dos dashboards** | Confirmado que o aluno vê apenas a Pesquisa da CPA e que Avaliação Docente e Egressos ficam restritos a coordenadores, avaliadores externos e CPA (RN02). Com os relatórios oficiais, a regra passou a valer para os relatórios de Professores e Corpo Técnico. |

---

## 3. Ajustes incorporados após a revisão

| Ponto avaliado | Necessidade identificada | Ajuste aplicado no projeto |
|---|---|---|
| **Atualização de dashboards** | Os links finais do Looker Studio serão inseridos pela própria CPA após a entrega. | Tabela `dashboards` no banco e formulário de gestão na página `/dashboards` (admin) para cadastrar e trocar os links e escolher os perfis, sem mexer no código. O portal aceita tanto o link de incorporação quanto o de compartilhamento. |
| **Acompanhamento de devolutivas** | Distinguir visualmente as ações concluídas das que ainda estão em andamento. | Campo `status` (*Planejado*, *Em andamento*, *Concluído*) com etiquetas coloridas nos cards e filtro por status no mural. |
| **Catalogação de relatórios** | Facilitar a busca de documentos por ciclo avaliativo durante as visitas dos avaliadores do MEC. | Campos `categoria` (Relatório de Autoavaliação / Boletim Informativo) e `ano_referencia` na tabela `documentos`, exibidos na tela e usados nos filtros. |
| **Consistência visual** | As telas de cada perfil tinham estilos diferentes entre si. | Padronização em um layout único e responsivo, com o mesmo menu, cores e componentes em todas as páginas. |
