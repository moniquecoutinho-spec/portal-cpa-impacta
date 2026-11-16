# Modelagem do Banco de Dados (MER e Dicionário de Dados)
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 2 — Modelagem e Design  
**SGBD:** MySQL / MariaDB (Banco: `portal_cpa`)  
Integrante 1: Monique Lima RA:2503159
Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307
Integrante 3: Alicya Sayuri Gallano Azato RA:2500140

---

## 1. Arquitetura Relacional e Regras de Integridade
O banco de dados relacional foi estruturado para garantir o isolamento de permissões por perfil e a atualização dinâmica dos conteúdos sem necessidade de alteração no código-fonte:

- **Relacionamento 1:N (`perfis` → `usuarios`):** Cada perfil de acesso pode estar vinculado a múltiplos usuários, enquanto cada usuário possui obrigatoriamente um único perfil ativo através da chave estrangeira `perfil_id`.
- **Controle de Visibilidade (`dashboards`):** Utiliza colunas booleanas (`visivel_aluno`, `visivel_coordenador`, `visivel_avaliador`) para filtrar dinamicamente quais painéis do Google Data Studio são exibidos para cada nível de usuário.
- **Transparência Pública (`devolutivas` e `relatorios`):** Tabelas estruturadas para leitura pública irrestrita e escrita exclusiva pelo perfil Administrador (CPA).

## 2. Diagrama Entidade-Relacionamento (DER)

```text
+------------------+         +-----------------------+
|      perfis      |         |       usuarios        |
+------------------+         +-----------------------+
| PK id            |1-------*| PK id                 |
|    nome          |         |    nome               |
|    descricao     |         |    email (UNIQUE)     |
+------------------+         |    matricula          |
                             |    senha_hash         |
                             | FK perfil_id          |
                             |    ativo              |
                             |    criado_em          |
                             +-----------------------+

+----------------------------------+   +---------------------------+   +---------------------------+
|            dashboards            |   |        devolutivas        |   |        relatorios         |
+----------------------------------+   +---------------------------+   +---------------------------+
| PK id                            |   | PK id                     |   | PK id                     |
|    titulo                        |   |    titulo                 |   |    titulo                 |
|    descricao                     |   |    area_responsavel       |   |    descricao              |
|    url_embed                     |   |    demanda_identificada   |   |    tipo (ENUM)            |
|    visivel_aluno (TINYINT)       |   |    acao_realizada         |   |    ano_referencia (YEAR)  |
|    visivel_coordenador (TINYINT) |   |    status (ENUM)          |   |    arquivo_nome           |
|    visivel_avaliador (TINYINT)   |   |    data_publicacao        |   |    data_upload            |
|    atualizado_em                 |   +---------------------------+   +---------------------------+
+----------------------------------+
