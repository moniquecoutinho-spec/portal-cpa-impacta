# Especificação de Requisitos — Portal CPA Faculdade Impacta
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA)  
**Instituição:** Faculdade Impacta  
**Tecnologias:** HTML5, Python (Flask) e MySQL  
**Data:** Novembro de 2026  

---

## 1. Objetivo do Sistema
Centralizar os resultados das avaliações institucionais da CPA em um portal web responsivo e com controle de acesso por perfil, reunindo dashboards do Google Data Studio (Looker Studio), mural público de devolutivas, repositório de relatórios/boletins e canais de atendimento.

## 2. Matriz de Perfis e Permissões
| Funcionalidade | Visitante (Público) | Aluno | Coordenador | Avaliador Externo (MEC) | Admin (CPA) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mural de Devolutivas** | Leitura | Leitura | Leitura | Leitura | Leitura + Criar/Editar/Excluir |
| **Relatórios e Boletins (PDF)** | Download | Download | Download | Download | Download + Upload/Excluir |
| **Página de Contato (Chat/Meet)** | Acesso | Acesso | Acesso | Acesso | Acesso |
| **Dashboard: Pesquisa CPA** | Bloqueado | Visualizar | Visualizar | Visualizar | Visualizar + Gerenciar |
| **Dashboard: Avaliação Docente** | Bloqueado | Bloqueado | Visualizar | Visualizar | Visualizar + Gerenciar |
| **Dashboard: Egressos** | Bloqueado | Bloqueado | Visualizar | Visualizar | Visualizar + Gerenciar |

## 3. Requisitos Funcionais (RF)
* **RF01 — Login e Autenticação:** Validar acesso por e-mail e senha, identificando o perfil do usuário e iniciando sessão segura.
* **RF02 — Controle de Acesso por Perfil:** Bloquear a visualização e o acesso direto por URL a dashboards não autorizados para o perfil logado.
* **RF03 — Exibição de Dashboards:** Incorporar os painéis do Google Data Studio (Looker Studio) via `<iframe>` responsivo conforme a matriz de permissões.
* **RF04 — Gestão de Dashboards (Admin):** Permitir que o Administrador da CPA cadastre ou atualize os links (`url_embed`) dos dashboards pelo painel, sem alterar código.
* **RF05 — Mural Público de Devolutivas:** Exibir publicamente as demandas levantadas nas pesquisas, a área responsável, a ação tomada, o status e a data.
* **RF06 — Gestão de Devolutivas (Admin):** Permitir que o Administrador da CPA publique, edite e exclua devolutivas.
* **RF07 — Repositório de Relatórios e Boletins:** Listar e permitir o download público de arquivos PDF organizados por categoria e ano.
* **RF08 — Upload de Relatórios (Admin):** Permitir o envio de novos documentos `.pdf` pelo Administrador da CPA.
* **RF09 — Página de Contato:** Exibir canais oficiais da CPA com botões de acesso direto ao **Google Chat** e **Google Meet**.

## 4. Requisitos Não Funcionais (RNF)
* **RNF01 — Responsividade:** Adaptação automática das telas e dashboards para computadores, tablets e celulares.

## 5. Catálogo Inicial de Dashboards e Documentos (Fase 1)

### 5.1 Dashboards Mapeados (Google Data Studio / Looker Studio)
| ID | Nome do Dashboard | Público Autorizado | Status da Integração |
| :--- | :--- | :--- | :--- |
| **DASH-01** | Pesquisa Institucional CPA | Alunos, Coordenadores, Avaliadores MEC, Admin | Aguardando link oficial da CPA (em teste com link modelo) |
| **DASH-02** | Avaliação Docente por Curso | Coordenadores, Avaliadores MEC, Admin | Aguardando link oficial da CPA (em teste com link modelo) |
| **DASH-03** | Acompanhamento de Egressos | Coordenadores, Avaliadores MEC, Admin | Aguardando link oficial da CPA (em teste com link modelo) |

### 5.2 Documentos Institucionais Mapeados
| Categoria | Exemplos de Arquivos | Formato | Acesso |
| :--- | :--- | :---: | :--- |
| **Relatórios de Autoavaliação** | Relatório Anual CPA, Relatório Parcial de Ciclo | `.pdf` | Público (Download) / Admin (Upload) |
| **Boletins Informativos** | Boletim de Resultados Semestrais, Informativo CPA | `.pdf` | Público (Download) / Admin (Upload) |
* **RNF02 — Segurança:** Senhas armazenadas com criptografia (`hash`) no MySQL e proteção contra *SQL Injection* no backend Python.
* **RNF03 — Usabilidade:** Navegação intuitiva com acesso às áreas públicas em no máximo 2 cliques.
* **RNF04 — Versionamento:** Código-fonte, scripts SQL e documentação armazenados em repositório público no GitHub.
