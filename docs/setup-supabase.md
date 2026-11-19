# Configuração do Supabase

Guia de referência para conectar o ambiente de desenvolvimento ao projeto Supabase do Portal CPA.

- **Project ref:** `tgtwvcegopwqihkjrlzf`
- **URL da API:** `https://tgtwvcegopwqihkjrlzf.supabase.co`
- **Chaves e senha:** ficam somente no arquivo `.env` (não versionado). Use `.env.example` como modelo.

---

## 1. Variáveis de ambiente

```bash
cp .env.example .env
```

| Variável | Onde usar | Observação |
|---|---|---|
| `SUPABASE_URL` | Front e backend | Pública |
| `SUPABASE_PUBLISHABLE_KEY` | Front e backend | Pública; a segurança vem da RLS |
| `SUPABASE_SECRET_KEY` | **Somente backend** | Ignora a RLS. Nunca enviar ao navegador nem ao Git |
| `SUPABASE_JWKS_URL` | Backend | Valida os JWT do Supabase Auth |
| `SUPABASE_DB_*` | Backend / ferramentas SQL | Conexão direta ao PostgreSQL |

**Conexão direta ao banco:**

```
host=db.tgtwvcegopwqihkjrlzf.supabase.co
port=5432
database=postgres
user=postgres
```

> O host direto `db.<ref>.supabase.co` usa IPv6. Se a rede não tiver IPv6, use a string do **Session Pooler** (Dashboard › Connect), que funciona em IPv4.

---

## 2. Aplicar o schema no projeto remoto

```bash
supabase login
supabase link --project-ref tgtwvcegopwqihkjrlzf
supabase db push --linked   # aplica supabase/migrations/ no projeto remoto
```

Os 4 dashboards oficiais da CPA são criados pela própria migration `20261119000000_dashboards_oficiais.sql`; não é preciso rodar o seed em produção.
As devolutivas de exemplo ficam em `supabase/seed.sql`, que o `db push` não executa: para tê-las no banco remoto, cole o `insert` no SQL Editor.

---

## 3. Se uma chave vazar

Se o `.env` for commitado por engano ou a chave secreta for exposta:

1. Dashboard › Project Settings › **API Keys** › gere uma nova secret key e revogue a antiga.
2. Atualize o `.env`.
3. Remova o arquivo do histórico do Git.
