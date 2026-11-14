# Especificação de Requisitos Funcionais e Não Funcionais
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 1 — Levantamento de Requisitos  
**Integrantes:**  Integrante 1: Monique Lima RA:2503159 Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307 Integrante 3: Alicya Sayuri Gallano Azato RA:2500140
**Data:** Novembro de 2026  

---

## 1. Requisitos Funcionais (RF)
- **RF01 — Autenticação de Usuários:** O sistema deve fornecer uma tela de login com validação por e-mail institucional e senha, iniciando uma sessão segura e identificando automaticamente o perfil do usuário.
- **RF02 — Controle de Acesso Baseado em Perfil:** O portal deve restringir a exibição de menus e bloquear o acesso via URL direta a páginas ou dashboards não autorizados para o perfil autenticado.
- **RF03 — Exibição de Dashboards por Perfil:** Na área logada, o sistema deve carregar os dashboards do Google Data Studio (Looker Studio) via incorporação (`<iframe>`), filtrando os painéis conforme o perfil do usuário.
- **RF04 — Gerenciamento Dinâmico de Dashboards (Admin):** O perfil Administrador (CPA) deve possuir uma interface para cadastrar, editar ou substituir as URLs de incorporação dos dashboards sem necessidade de alteração no código-fonte.
- **RF05 — Mural Público de Devolutivas:** O sistema deve exibir publicamente (sem necessidade de login) os registros contendo o título da demanda identificada nas pesquisas, a área responsável, a ação/resposta executada, o status (Planejado, Em andamento, Concluído) e a data de publicação.
- **RF06 — Gestão do Mural de Devolutivas (Admin):** O Administrador (CPA) deve poder publicar, editar e remover registros no Mural de Devolutivas.
- **RF07 — Repositório de Relatórios e Boletins:** O sistema deve listar publicamente os documentos institucionais (Relatórios de Autoavaliação e Boletins Informativos) organizados por ano e categoria, permitindo visualização e download em formato PDF.
- **RF08 — Upload de Relatórios e Boletins (Admin):** O Administrador (CPA) deve poder enviar novos arquivos PDF ao repositório informando título, descrição, categoria e ano de referência.
- **RF09 — Página de Contato e Atendimento:** O portal deve disponibilizar uma página pública com informações institucionais da CPA e botões de redirecionamento direto para atendimento via Google Chat e Google Meet.

## 2. Requisitos Não Funcionais (RNF)
- **RNF01 — Responsividade:** Todas as páginas e dashboards incorporados devem se adaptar automaticamente a telas de desktops, notebooks, tablets e smartphones.
- **RNF02 — Segurança da Informação:** As senhas devem ser armazenadas exclusivamente em formato criptografado (hash) no banco de dados MySQL, e todas as consultas devem utilizar consultas parametrizadas para prevenção contra SQL Injection.
- **RNF03 — Usabilidade:** Navegação intuitiva com contraste adequado e acesso a qualquer seção pública em no máximo 2 cliques.
- **RNF04 — Compatibilidade:** O portal deve funcionar corretamente nas versões atuais dos navegadores Google Chrome, Mozilla Firefox, Microsoft Edge e Safari.
- **RNF05 — Manutenibilidade e Versionamento:** Todo o código-fonte, scripts de banco de dados e documentação técnica devem ser versionados em repositório público no GitHub.
- **RNF06 — Stack Tecnológica:** O sistema deve ser desenvolvido utilizando HTML5, CSS3, JavaScript no front-end, Python (Flask) no back-end e MySQL como sistema gerenciador de banco de dados.

## 3. Regras de Negócio (RN)
- **RN01 — Acesso Público Irrestrito à Transparência:** O Mural de Devolutivas, a Área de Relatórios/Boletins e a Página de Contato nunca devem exigir login, garantindo o cumprimento das diretrizes legais de publicidade do MEC.
- **RN02 — Isolamento de Dados Sensíveis:** Os dashboards de Avaliação Docente e Egressos são restritos a Coordenadores, Avaliadores Externos e Administradores da CPA, não podendo ser listados ou acessados por alunos.
- **RN03 — Visão Integral para Avaliação Externa:** O perfil Avaliador Externo (MEC) possui permissão de leitura irrestrita sobre todos os dashboards ativos no sistema, sem permissão de alteração de dados.
- **RN04 — Formato de Documentos:** A área de relatórios aceitará exclusivamente arquivos no formato PDF (`.pdf`) para garantir compatibilidade universal de leitura.
