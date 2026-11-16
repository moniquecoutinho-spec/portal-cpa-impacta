# Estrutura de Navegação e Arquitetura de Layout Responsivo
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 2 — Modelagem e Design  
Integrante 1: Monique Lima RA:2503159
Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307
Integrante 3: Alicya Sayuri Gallano Azato RA:2500140

# Protótipos de Interface por Perfil de Usuário
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 2 — Modelagem e Design  
**Formato:** Protótipos Navegáveis em HTML5 e CSS3  
**Integrantes:** [Nome 1 - RA] | [Nome 2 - RA] | [Nome 3 - RA]  
**Data:** 15/11/2026  

---

## 1. Abordagem de Prototipação
Para acelerar a validação visual com os envolvidos e garantir fidelidade técnica, a equipe desenvolveu protótipos navegáveis diretamente em **HTML5 e CSS3**. Essa abordagem permitiu testar o fluxo de navegação, a hierarquia das informações e o comportamento responsivo antes da integração com o banco de dados MySQL.

## 2. Detalhamento das Interfaces por Perfil de Acesso

### 2.1 Perfil 1 — Visitante (Área Pública sem Autenticação)
- **Página Inicial (`index.html`):** Apresentação institucional da CPA, indicadores de transparência e atalhos rápidos para o Mural de Devolutivas, Relatórios e Login.
- **Mural de Devolutivas (`devolutivas.html`):** Cards organizados cronologicamente exibindo a área responsável, a demanda apontada na avaliação, a resposta institucional e uma etiqueta visual de status (`Planejado`, `Em andamento` ou `Concluído`).
- **Relatórios e Boletins (`relatorios.html`):** Repositório público filtrado por categoria e ano de referência, com botão direto para download do PDF.
- **Página de Contato (`contato.html`):** Informações de atendimento da coordenação da CPA com botões de acesso direto ao **Google Chat** e **Google Meet**.

### 2.2 Tela de Autenticação (`login.html`)
- Formulário centralizado com validação de e-mail institucional e senha, exibindo alertas claros em caso de credenciais inválidas e redirecionando automaticamente o usuário para a visão correspondente ao seu perfil.

### 2.3 Perfil 2 — Aluno (Presencial e EAD)
- Após o login, a barra superior identifica o usuário como `Aluno` e a área de dashboards (`dashboards.html`) carrega exclusivamente o painel da **Pesquisa Institucional da CPA** em formato responsivo.

### 2.4 Perfil 3 — Coordenador de Curso
- Além da Pesquisa Institucional da CPA, a interface habilita a visualização dos painéis analíticos de **Avaliação Docente por Curso** e **Acompanhamento de Egressos**, permitindo análise comparativa dos indicadores acadêmicos.

### 2.5 Perfil 4 — Avaliador Externo (MEC)
- Exibe todos os dashboards ativos no portal em modo integral de leitura para fins de auditoria e avaliação regulatória, mantendo ocultos os controles de edição ou exclusão.

### 2.6 Perfil 5 — Administrador (CPA)
- Além de visualizar todos os dashboards, habilita formulários de gestão diretamente nas respectivas telas:
  - Cadastro e remoção de links de dashboards do Google Data Studio com seleção de visibilidade por perfil.
  - Publicação e exclusão de registros no Mural de Devolutivas.
  - Upload e remoção de arquivos `.pdf` na área de Relatórios e Boletins.
