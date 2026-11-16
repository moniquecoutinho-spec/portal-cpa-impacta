# Registro de Validação dos Protótipos e Ajustes de Design
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 2 — Modelagem e Design  
**Integrantes:** [Nome 1 - RA] | [Nome 2 - RA] | [Nome 3 - RA]  
**Data:** 15/11/2026  

---

## 1. Objetivo e Escopo da Validação
Avaliar os protótipos de tela em HTML/CSS e a estrutura relacional do banco de dados frente aos requisitos levantados na Fase 1, assegurando que todos os perfis de usuário tenham seus fluxos atendidos de forma clara e intuitiva antes da integração final com o back-end em Python.

## 2. Aspectos Validados
- **Transparência Pública:** Confirmado que o Mural de Devolutivas, os Relatórios em PDF e a Página de Contato funcionam sem exigência de login, atendendo às normas de publicidade institucional.
- **Clareza na Identificação de Perfil:** Aprovada a exibição do nome e do perfil ativo no cabeçalho após o login, orientando o usuário sobre seu nível de acesso.
- **Canais de Atendimento:** Validada a disposição dos botões diretos para Google Chat e Google Meet na página de contato.

## 3. Ajustes Incorporados após Revisão
| Ponto Avaliado | Necessidade Identificada | Ajuste Aplicado no Projeto |
| :--- | :--- | :--- |
| **Atualização de Dashboards** | Os links finais do Google Data Studio serão inseridos pela própria CPA após a entrega. | Implementada tabela `dashboards` no MySQL e formulário no painel Admin para cadastro e troca de URLs sem mexer no código. |
| **Acompanhamento de Devolutivas** | Necessidade de distinguir visualmente ações já concluídas daquelas ainda em andamento. | Incluído o campo `status` (`Planejado`, `Em andamento`, `Concluído`) com etiquetas coloridas nos cards do mural. |
| **Catalogação de Relatórios** | Facilitar a busca de documentos por ciclo avaliativo durante visitas de avaliadores do MEC. | Adicionados os campos `tipo` (`Relatório de Autoavaliação` / `Boletim`) e `ano_referencia` na tabela e na exibição da tela. |
