# Especificação de Requisitos Funcionais e Não Funcionais

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 1 — Levantamento de Requisitos
> **Data:** Novembro de 2026

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

---

## 1. Requisitos Funcionais (RF)

| ID | Requisito | Descrição |
|---|---|---|
| **RF01** | Autenticação de usuários | Tela de login com validação por e-mail institucional e senha, iniciando uma sessão segura e identificando automaticamente o perfil do usuário. |
| **RF02** | Controle de acesso por perfil | Restringir a exibição de menus e bloquear o acesso via URL direta a páginas ou dashboards não autorizados para o perfil autenticado. |
| **RF03** | Exibição de dashboards por perfil | Na área logada, carregar os dashboards do Looker Studio via `<iframe>`, filtrando os painéis conforme o perfil do usuário. |
| **RF04** | Gerenciamento dinâmico de dashboards (Admin) | Interface para cadastrar, editar ou substituir as URLs de incorporação sem alteração no código-fonte. |
| **RF05** | Mural público de devolutivas | Exibir publicamente, sem login, os registros com título da demanda, área responsável, ação executada, status (*Planejado*, *Em andamento*, *Concluído*) e data de publicação. |
| **RF06** | Gestão do mural de devolutivas (Admin) | Publicar, editar e remover registros do Mural de Devolutivas. |
| **RF07** | Repositório de relatórios e boletins | Listar publicamente os documentos institucionais, organizados por ano e categoria, com visualização e download em PDF. |
| **RF08** | Upload de relatórios e boletins (Admin) | Enviar novos PDFs informando título, descrição, categoria e ano de referência. |
| **RF09** | Página de contato e atendimento | Página pública com informações da CPA e botões para atendimento via Google Chat e Google Meet. |

---

## 2. Requisitos Não Funcionais (RNF)

| ID | Requisito | Descrição |
|---|---|---|
| **RNF01** | Responsividade | Todas as páginas e dashboards incorporados se adaptam a desktops, notebooks, tablets e smartphones. |
| **RNF02** | Segurança da informação | Senhas armazenadas exclusivamente com hash; todas as consultas parametrizadas para prevenir SQL Injection. |
| **RNF03** | Usabilidade | Navegação intuitiva, contraste adequado e acesso a qualquer seção pública em no máximo **2 cliques**. |
| **RNF04** | Compatibilidade | Funcionar nas versões atuais de Google Chrome, Mozilla Firefox, Microsoft Edge e Safari. |
| **RNF05** | Manutenibilidade e versionamento | Código-fonte, scripts de banco e documentação técnica versionados em repositório público no GitHub. |
| **RNF06** | Stack tecnológica | HTML5, CSS3 e JavaScript no front-end; Python (Flask) no back-end; banco de dados relacional. |

> **Atualização do RNF06:** a especificação original previa **MySQL**. O projeto adotou **PostgreSQL via Supabase** (com Supabase Auth e Storage), mantendo Flask e o front-end. Os RNF02 passam a ser atendidos pelo Supabase Auth (hash bcrypt) e pela API parametrizada do Supabase.

---

## 3. Regras de Negócio (RN)

| ID | Regra | Descrição |
|---|---|---|
| **RN01** | Acesso público irrestrito à transparência | Mural de Devolutivas, Relatórios/Boletins e Contato **nunca** exigem login, em cumprimento às diretrizes de publicidade do MEC. |
| **RN02** | Isolamento de dados sensíveis | Dashboards de Avaliação Docente e Egressos são restritos a Coordenadores, Avaliadores Externos e Administradores; **não podem ser listados nem acessados por alunos**. |
| **RN03** | Visão integral para avaliação externa | O Avaliador Externo (MEC) tem leitura irrestrita de todos os dashboards ativos, sem permissão de alteração. |
| **RN04** | Formato de documentos | A área de relatórios aceita **exclusivamente PDF**, garantindo compatibilidade universal de leitura. |
