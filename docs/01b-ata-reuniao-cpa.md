# Registro de Alinhamento e Fluxos de Trabalho — CPA Impacta
**Fase:** 1 — Levantamento de Requisitos  
**Participantes:** Equipe de Desenvolvimento (3 integrantes) e Representante CPA / IPC  

---

## 1. Resumo do Entendimento e Fluxos de Trabalho
Durante o levantamento inicial do escopo com a instituição, foram definidos os fluxos operacionais que o portal deverá atender:

1. **Fluxo de Publicação de Dashboards:** A CPA produz os painéis analíticos no Google Data Studio (Looker Studio). O Administrador da CPA inserirá os links de incorporação no painel administrativo do portal, que distribuirá automaticamente a visualização conforme o perfil logado (Aluno, Coordenador ou Avaliador Externo MEC).
2. **Fluxo de Devolutivas Institucionais:** Após o fechamento de cada ciclo avaliativo, a equipe da CPA registrará no portal as demandas apontadas pelos alunos/docentes e as ações corretivas executadas pelas áreas. A visualização será aberta ao público sem necessidade de login.
3. **Fluxo de Relatórios e Boletins:** Documentos oficiais (PDF) serão enviados pelo Administrador da CPA para ficarem disponíveis para download público organizado por ano e categoria.
4. **Fluxo de Atendimento à Comunidade:** O portal centralizará os links institucionais para contato direto via **Google Chat** e **Google Meet**, respeitando os horários de disponibilidade da coordenação da CPA.

## 2. Definições e Pendências Registradas
* **Definição Técnica:** Adotada arquitetura web com **HTML5, CSS3, JavaScript, Python (Flask) e MySQL**, permitindo gestão dinâmica dos links sem necessidade de alteração no código-fonte.
* **Pendência Externa (CPA):** Os links oficiais dos dashboards do Google Data Studio ainda serão fornecidos pela CPA. Ficou alinhado que o desenvolvimento e os testes de permissão serão conduzidos utilizando links de demonstração do Looker Studio, com campo editável no painel administrativo para substituição imediata assim que forem enviados.
