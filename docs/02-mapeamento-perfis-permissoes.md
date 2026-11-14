# Mapeamento de Perfis de Usuário e Permissões de Acesso
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 1 — Levantamento de Requisitos  
 Integrante 1: Monique Lima RA:2503159 Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307 Integrante 3: Alicya Sayuri Gallano Azato RA:2500140
**Data:** Novembro de 2026  

---

## 1. Descrição dos Perfis de Acesso
- **Visitante (Público Geral):** Qualquer membro da comunidade externa ou interna sem necessidade de autenticação. Possui acesso apenas às áreas de transparência pública (Página Inicial, Mural de Devolutivas, Relatórios/Boletins e Contato).
- **Aluno (Presencial e EAD):** Estudante regularmente matriculado na instituição. Além das áreas públicas, tem acesso autenticado ao dashboard geral da Pesquisa Institucional da CPA.
- **Coordenador de Curso:** Gestor acadêmico responsável pelos cursos. Além das áreas públicas e da Pesquisa da CPA, visualiza os dashboards de Avaliação Docente e de Acompanhamento de Egressos.
- **Avaliador Externo (MEC):** Representante designado pelo Ministério da Educação para processos regulatórios. Possui acesso integral de leitura a todos os dashboards e documentos institucionais, sem permissão de edição.
- **Administrador (CPA):** Membro da Comissão Própria de Avaliação responsável pela gestão do portal. Possui acesso total aos dashboards e permissão exclusiva para publicar/excluir devolutivas, fazer upload de relatórios PDF e gerenciar os links dos dashboards.

## 2. Matriz de Permissões por Funcionalidade

| Funcionalidade / Módulo | Visitante (Sem Login) | Aluno (Presencial/EAD) | Coordenador de Curso | Avaliador Externo (MEC) | Administrador (CPA) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Página Inicial Institucional** | Acesso total | Acesso total | Acesso total | Acesso total | Acesso total |
| **Mural de Devolutivas** | Leitura | Leitura | Leitura | Leitura | Leitura + Criar/Editar/Excluir |
| **Relatórios e Boletins (PDF)** | Visualizar e Baixar | Visualizar e Baixar | Visualizar e Baixar | Visualizar e Baixar | Visualizar/Baixar + Upload/Excluir |
| **Página de Contato (Chat/Meet)** | Acesso total | Acesso total | Acesso total | Acesso total | Acesso total |
| **Dashboard: Pesquisa da CPA** | Bloqueado | Visualizar | Visualizar | Visualizar | Visualizar + Gerenciar Link |
| **Dashboard: Avaliação Docente** | Bloqueado | Bloqueado | Visualizar | Visualizar | Visualizar + Gerenciar Link |
| **Dashboard: Pesquisa de Egressos** | Bloqueado | Bloqueado | Visualizar | Visualizar | Visualizar + Gerenciar Link |
| **Gestão de Usuários e Perfis** | Bloqueado | Bloqueado | Bloqueado | Bloqueado | Acesso total |

## 3. Regras de Controle e Isolamento de Acesso
- **Bloqueio por Sessão:** Tentativas de acesso direto via URL aos dashboards sem login ativo redirecionam automaticamente para a tela de autenticação.
- **Filtragem Dinâmica:** O backend em Python consulta o `perfil_id` do usuário no banco MySQL e renderiza exclusivamente os painéis autorizados para aquele nível.
