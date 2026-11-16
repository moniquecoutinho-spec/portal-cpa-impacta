# Desenvolvimento da Página Inicial e Dashboards Dinâmicos e Responsivos
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 3 — Desenvolvimento do Portal  
Integrante 1: Monique Lima RA:2503159
Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307
Integrante 3: Alicya Sayuri Gallano Azato RA:2500140

---

## 1. Estrutura da Página Inicial (`index.html`)
A página inicial foi projetada como porta de entrada institucional da CPA para toda a comunidade acadêmica, reunindo:
- **Cabeçalho Institucional:** Apresentação clara do papel da Comissão Própria de Avaliação na melhoria contínua da Faculdade Impacta.
- **Cartões de Acesso Rápido:** Atalhos diretos para as seções públicas (Mural de Devolutivas, Relatórios e Boletins em PDF, Página de Contato) e botão de destaque para acesso à Área Restrita (Dashboards).
- **Indicadores de Transparência:** Resumo visual dos ciclos avaliativos e canais de participação abertos aos alunos, docentes e avaliadores externos.

## 2. Renderização Dinâmica e Responsiva dos Dashboards (`dashboards.html`)
Na área logada, a exibição dos painéis adapta-se dinamicamente tanto ao perfil do usuário quanto ao tamanho da tela do dispositivo:
- **Renderização Dinâmica:** O layout ajusta automaticamente a quantidade de painéis exibidos conforme o retorno do banco de dados MySQL, exibindo mensagem informativa caso nenhum dashboard esteja atribuído ao perfil.
- **Contêineres Responsivos:** Cada painel do Google Data Studio é encapsulado em um contêiner fluido (`width: 100%`) com altura proporcional ajustada por media queries, eliminando cortes horizontais ou distorções em notebooks, tablets e smartphones.
- **Navegação Adaptativa:** A barra superior converte-se automaticamente em menu retrátil em telas móveis, mantendo visível a identificação do usuário logado e o botão de saída.
