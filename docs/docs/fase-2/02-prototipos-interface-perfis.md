# Estrutura de Navegação e Arquitetura de Layout Responsivo
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 2 — Modelagem e Design  
Integrante 1: Monique Lima RA:2503159
Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307
Integrante 3: Alicya Sayuri Gallano Azato RA:2500140

---

## 1. Mapa de Navegação (Arquitetura da Informação)

```text
Portal CPA Impacta
├── [Público] Início (index.html)
├── [Público] Mural de Devolutivas (devolutivas.html)
│     └── [Apenas Admin CPA] Formulário de Nova Devolutiva / Excluir
├── [Público] Relatórios e Boletins (relatorios.html)
│     └── [Apenas Admin CPA] Formulário de Upload PDF / Excluir
├── [Público] Contato CPA (contato.html)
│     ├── Link Externo: Google Chat
│     └── Link Externo: Google Meet
└── [Autenticação] Entrar / Login (login.html)
      └── [Área Logada] Dashboards Analíticos (dashboards.html)
            ├── Perfil Aluno: Pesquisa CPA
            ├── Perfil Coordenador: Pesquisa CPA + Avaliação Docente + Egressos
            ├── Perfil Avaliador MEC: Todos os Dashboards (Leitura)
            └── Perfil Admin CPA: Todos os Dashboards + Gestão de Links Embed



2. Tabela de Fluxo e Níveis de AcessoNível / SeçãoPáginaAcesso ExigidoFuncionalidades DisponíveisNível 1 (Menu Principal)Início (index.html)PúblicoVisão geral da CPA e atalhos rápidos.Nível 1 (Menu Principal)Mural de Devolutivas (devolutivas.html)Público (Admin edita)Consulta de respostas das áreas; publicação/exclusão pelo Admin.Nível 1 (Menu Principal)Relatórios e Boletins (relatorios.html)Público (Admin edita)Download de PDFs institucionais; upload/exclusão pelo Admin.Nível 1 (Menu Principal)Contato CPA (contato.html)PúblicoRedirecionamento para Google Chat e Google Meet.Nível 1 (Ação Superior)Login (login.html)PúblicoAutenticação por e-mail e senha.Nível 2 (Área Restrita)Dashboards (dashboards.html)Autenticado (Por Perfil)Exibição de painéis Google Data Studio conforme permissões.3. Padrão de Navegação e Componentes FixosBarra de Navegação Superior (Navbar): Mantida fixa no topo de todas as páginas para consistência visual, contendo a identidade da Faculdade Impacta/CPA à esquerda, os links de seção ao centro e o controle de sessão à direita (botão Entrar quando deslogado; nome do usuário, etiqueta do perfil e botão Sair quando autenticado).Feedback Visual: Exibição de mensagens de alerta no topo da área de conteúdo para confirmar ações realizadas (login efetuado, publicação de devolutiva, envio de relatório ou bloqueio de acesso não autorizado).4. Especificação de Layout ResponsivoTipo de DispositivoLargura de TelaAdaptação da InterfaceDesktop / NotebookAcima de 992pxMenu horizontal completo; exibição de cards em grade de 2 a 3 colunas; dashboards do Google Data Studio em proporção widescreen.TabletEntre 768px e 991pxReorganização automática para grade de 2 colunas; redimensionamento proporcional dos containers de dashboards sem rolagem lateral.Smartphone (Mobile)Abaixo de 768pxMenu recolhido em botão expansível; cards empilhados em coluna única (100% de largura); botões de ação e links de contato ampliados para toque.5. Adaptação dos Dashboards IncorporadosOs painéis do Google Data Studio (Looker Studio) são inseridos dentro de containers responsivos (width: 100% com altura proporcional ajustável), evitando cortes nas visualizações gráficas em telas menores.
