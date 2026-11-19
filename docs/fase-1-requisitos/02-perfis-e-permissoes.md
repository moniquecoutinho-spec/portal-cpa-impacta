# Mapeamento de Perfis de Usuário e Permissões de Acesso

> **Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta
> **Etapa:** Fase 1 — Levantamento de Requisitos
> **Data:** Novembro de 2026

| Integrante | Nome | RA |
|---|---|---|
| 1 | Monique Lima | 2503159 |
| 2 | Vitor Gabriel Ribeiro dos Santos | 2501307 |
| 3 | Alicya Sayuri Gallano Azato | 2500140 |

---

## 1. Descrição dos perfis de acesso

| Perfil | Quem é | O que acessa |
|---|---|---|
| 🌐 **Visitante** (público geral) | Qualquer pessoa da comunidade interna ou externa, sem autenticação | Apenas as áreas de transparência pública: Página Inicial, Mural de Devolutivas, Relatórios/Boletins e Contato |
| 🎓 **Aluno** (Presencial e EAD) | Estudante regularmente matriculado | Áreas públicas + dashboard da **Pesquisa Institucional da CPA** |
| 🧑‍🏫 **Coordenador de Curso** | Gestor acadêmico responsável pelos cursos | Áreas públicas + Pesquisa da CPA + dashboards de **Avaliação Docente** e **Egressos** |
| 🏛️ **Avaliador Externo (MEC)** | Representante do Ministério da Educação em processos regulatórios | Leitura integral de **todos** os dashboards e documentos, sem edição |
| 🛠️ **Administrador (CPA)** | Membro da CPA responsável pela gestão do portal | Acesso total; exclusivo para publicar/excluir devolutivas, enviar PDFs e gerenciar links dos dashboards |

---

## 2. Matriz de permissões por funcionalidade

**Legenda:** ✅ acesso total · 👁️ visualizar · ⬇️ visualizar e baixar · ✏️ gerenciar · ❌ bloqueado

| Funcionalidade | Visitante | Aluno | Coordenador | Avaliador MEC | Admin CPA |
|---|:-:|:-:|:-:|:-:|:-:|
| Página Inicial Institucional | ✅ | ✅ | ✅ | ✅ | ✅ |
| Mural de Devolutivas | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ ✏️ criar/editar/excluir |
| Relatórios e Boletins (PDF) | ⬇️ | ⬇️ | ⬇️ | ⬇️ | ⬇️ ✏️ upload/excluir |
| Página de Contato (Chat/Meet) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dashboard: Pesquisa da CPA | ❌ | 👁️ | 👁️ | 👁️ | 👁️ ✏️ gerenciar link |
| Dashboard: Avaliação Docente | ❌ | ❌ | 👁️ | 👁️ | 👁️ ✏️ gerenciar link |
| Dashboard: Pesquisa de Egressos | ❌ | ❌ | 👁️ | 👁️ | 👁️ ✏️ gerenciar link |
| Gestão de Usuários e Perfis | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 3. Regras de controle e isolamento de acesso

| Regra | Descrição |
|---|---|
| **Bloqueio por sessão** | Tentativas de acesso direto via URL aos dashboards sem login ativo redirecionam automaticamente para a tela de autenticação. |
| **Filtragem dinâmica** | O backend consulta o perfil do usuário no banco de dados e exibe exclusivamente os painéis autorizados para aquele nível. |

> **Implementação:** além da checagem no backend Flask, a filtragem também é garantida no próprio banco por **Row Level Security** (ver `supabase/migrations/`).
