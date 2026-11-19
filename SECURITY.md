# Política de Segurança

## Como reportar uma vulnerabilidade

**Não abra uma issue pública.** Use o recurso
[Report a vulnerability](https://github.com/moniquecoutinho-spec/portal-cpa-impacta/security/advisories/new) na aba **Security** do repositório
ou contate diretamente os mantenedores.

Inclua, se possível:

- descrição do problema e impacto;
- passos para reproduzir;
- arquivos, rotas ou tabelas afetados.

O retorno inicial é feito em até 5 dias úteis.

## Escopo

| Área | Exemplos |
|---|---|
| Controle de acesso | Usuário vendo dashboard não autorizado, escalada de perfil |
| Banco de dados | Falhas de RLS, injeção de SQL |
| Segredos | Chaves do Supabase expostas |
| Upload de arquivos | Envio de arquivo que não seja PDF |

## Práticas adotadas

- Row Level Security em todas as tabelas, com testes automatizados (`supabase/tests/`).
- Segredos apenas em `.env` (não versionado); varredura com Gitleaks em cada PR.
- Dependabot para alertas e atualizações de dependências.
- CodeQL para análise estática quando habilitado.

## Se uma chave vazar

1. No Supabase Dashboard › Project Settings › **API Keys**, gere uma nova chave e revogue a antiga.
2. Atualize o `.env` local.
3. Remova o arquivo exposto do histórico do Git.
