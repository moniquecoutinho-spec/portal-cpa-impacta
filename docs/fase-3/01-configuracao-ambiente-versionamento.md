# Configuração do Ambiente de Desenvolvimento e Versionamento de Código
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 3 — Desenvolvimento do Portal  

Integrante 1: Monique Lima RA:2503159
Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307
Integrante 3: Alicya Sayuri Gallano Azato RA:2500140  

---

## 1. Arquitetura do Ambiente Local de Desenvolvimento
| Camada / Ferramenta | Tecnologia Adotada | Finalidade no Projeto |
| :--- | :--- | :--- |
| **Linguagem Back-end** | Python 3.x + Framework Flask | Gerenciamento de rotas, sessões de login, regras de perfil e upload de arquivos. |
| **Banco de Dados** | MySQL / MariaDB (`portal_cpa`) | Armazenamento relacional de usuários, perfis, links de dashboards, devolutivas e relatórios. |
| **Conector de Banco** | `mysql-connector-python` | Comunicação segura entre a aplicação Python e o servidor MySQL via consultas parametrizadas. |
| **Front-end** | HTML5, CSS3 e JavaScript | Estruturação das telas responsivas e renderização dinâmica via motor de templates Jinja2. |
| **Versionamento** | Git e GitHub | Controle de histórico, integração das entregas da equipe e hospedagem do código-fonte. |

## 2. Estrutura de Diretórios do Repositório (`portal-cpa-impacta`)
```text
portal-cpa-impacta/
├── docs/                 # Documentação técnica dividida por fases (fase-1, fase-2, fase-3...)
├── sql/                  # Script banco_cpa.sql (DDL e carga inicial)
├── static/               # CSS, JS, imagens e pasta uploads/ para PDFs
├── templates/            # Páginas HTML (index, login, dashboards, devolutivas, relatorios, contato)
├── app.py                # Aplicação principal back-end em Python (Flask)
└── requirements.txt      # Dependências Python do projeto
