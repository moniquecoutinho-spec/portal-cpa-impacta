# Integração dos Dashboards do Google Data Studio por Perfil
**Projeto:** Portal Web da Comissão Própria de Avaliação (CPA) — Faculdade Impacta  
**Etapa:** Fase 3 — Desenvolvimento do Portal  
Integrante 1: Monique Lima RA:2503159
Integrante 2: Vitor Gabriel Ribeiro dos Santos RA: 2501307
Integrante 3: Alicya Sayuri Gallano Azato RA:2500140

---

## 1. Arquitetura de Incorporação Dinâmica
Para permitir que os painéis criados no Google Data Studio (Looker Studio) sejam exibidos de forma centralizada e atualizados sem intervenção no código-fonte, a integração foi estruturada em três etapas:
- **Persistência no MySQL:** A tabela `dashboards` armazena o título, a descrição, a URL de incorporação (`url_embed`) gerada pelo Google Data Studio e as bandeiras de permissão por perfil (`visivel_aluno`, `visivel_coordenador`, `visivel_avaliador`).
- **Seleção no Back-end (`app.py`):** Quando o usuário acessa a rota `/dashboards`, o Python executa a consulta filtrada conforme o perfil armazenado na sessão e envia a lista de painéis permitidos ao template HTML.
- **Renderização Segura (`<iframe>`):** O template percorre a lista recebida e incorpora cada painel utilizando a tag `<iframe>` com atributos de segurança e redimensionamento automático.

## 2. Matriz de Exibição Aplicada na Integração
| Dashboard Integrado | Perfil Aluno | Perfil Coordenador | Perfil Avaliador MEC | Perfil Admin CPA |
| :--- | :---: | :---: | :---: | :---: |
| **Pesquisa Institucional CPA** | Exibido | Exibido | Exibido | Exibido + Gerenciar |
| **Avaliação Docente por Curso** | Oculto | Exibido | Exibido | Exibido + Gerenciar |
| **Acompanhamento de Egressos** | Oculto | Exibido | Exibido | Exibido + Gerenciar |

## 3. Painel de Gestão de Links (Exclusivo Admin CPA)
Na própria página `/dashboards`, o perfil Administrador visualiza um formulário superior onde pode cadastrar novos links de incorporação do Google Data Studio, definir quais perfis terão acesso por meio de caixas de seleção e remover painéis desatualizados.
