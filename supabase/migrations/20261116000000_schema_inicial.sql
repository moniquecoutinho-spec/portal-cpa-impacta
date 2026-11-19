-- =============================================================================
-- Portal CPA - Faculdade Impacta
-- Migration inicial: schema, funcoes auxiliares, triggers, RLS e storage.
--
-- Decisoes de modelagem (ver docs da Fase 1):
--   * Visitante (sem login) NAO e um perfil: e o papel "anon" do Supabase.
--   * Senhas ficam no Supabase Auth (auth.users, hash bcrypt) -> atende RNF02.
--   * Admin e Avaliador MEC enxergam todos os dashboards ativos por regra na
--     policy (RN03); por isso nao precisam de linhas em dashboard_perfis.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Tabelas de dominio (lookup)
-- -----------------------------------------------------------------------------

create table public.perfis (
  id         smallint generated always as identity primary key,
  codigo     text not null unique
             check (codigo in ('aluno', 'coordenador', 'avaliador_mec', 'admin')),
  nome       text not null,
  descricao  text
);

comment on table public.perfis is
  'Perfis autenticados. O Visitante e o papel anon, nao uma linha desta tabela.';

insert into public.perfis (codigo, nome, descricao) values
  ('aluno',         'Aluno (Presencial/EAD)', 'Acesso ao dashboard da Pesquisa Institucional da CPA.'),
  ('coordenador',   'Coordenador de Curso',   'Pesquisa da CPA, Avaliacao Docente e Egressos.'),
  ('avaliador_mec', 'Avaliador Externo (MEC)', 'Leitura integral de todos os dashboards ativos.'),
  ('admin',         'Administrador (CPA)',    'Gestao total do portal.')
on conflict (codigo) do nothing;

-- -----------------------------------------------------------------------------
-- 2. Usuarios (espelho de auth.users com perfil)
-- -----------------------------------------------------------------------------

create table public.usuarios (
  id          uuid primary key references auth.users (id) on delete cascade,
  nome        text not null,
  email       text not null unique,
  perfil_id   smallint not null references public.perfis (id),
  ativo       boolean not null default true,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create index usuarios_perfil_id_idx on public.usuarios (perfil_id);

comment on table public.usuarios is
  'Dados do portal por usuario. Nao ha coluna de senha: a autenticacao e do Supabase Auth.';

-- -----------------------------------------------------------------------------
-- 3. Funcoes auxiliares (dependem de usuarios/perfis, por isso vem depois)
-- -----------------------------------------------------------------------------

-- security definer evita recursao de RLS ao consultar public.usuarios
-- dentro de policies. Usuario inativo => retorna null (sem permissoes).
create or replace function public.perfil_atual()
returns text
language sql
stable
security definer
set search_path = ''
as $$
  select p.codigo
  from public.usuarios u
  join public.perfis p on p.id = u.perfil_id
  where u.id = auth.uid()
    and u.ativo
$$;

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select coalesce(public.perfil_atual() = 'admin', false)
$$;

revoke all on function public.perfil_atual() from public;
revoke all on function public.is_admin() from public;
grant execute on function public.perfil_atual() to anon, authenticated;
grant execute on function public.is_admin() to anon, authenticated;

create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- -----------------------------------------------------------------------------
-- 4. Demais tabelas
-- -----------------------------------------------------------------------------

-- Dashboards do Looker Studio (DASH-01..03)
create table public.dashboards (
  id          bigint generated always as identity primary key,
  codigo      text not null unique,
  nome        text not null,
  descricao   text,
  url_embed   text not null
              check (url_embed ~ '^https://(lookerstudio|datastudio)\.google\.com/'),
  ativo       boolean not null default true,
  ordem       smallint not null default 0,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  updated_by  uuid references public.usuarios (id) on delete set null
);

comment on column public.dashboards.url_embed is
  'URL de incorporacao (iframe). Restrita ao dominio do Looker Studio por seguranca.';

-- Quais perfis (alem de admin e avaliador_mec, que veem tudo) acessam cada dashboard
create table public.dashboard_perfis (
  dashboard_id  bigint   not null references public.dashboards (id) on delete cascade,
  perfil_id     smallint not null references public.perfis (id) on delete cascade,
  primary key (dashboard_id, perfil_id)
);

create index dashboard_perfis_perfil_id_idx on public.dashboard_perfis (perfil_id);

-- Mural de Devolutivas (publico)
create table public.devolutivas (
  id                bigint generated always as identity primary key,
  titulo            text not null,
  area_responsavel  text not null,
  acao              text not null,
  status            text not null default 'planejado'
                    check (status in ('planejado', 'em_andamento', 'concluido')),
  data_publicacao   date not null default current_date,
  created_by        uuid default auth.uid() references public.usuarios (id) on delete set null,
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now()
);

create index devolutivas_data_publicacao_idx on public.devolutivas (data_publicacao desc);

-- Relatorios e Boletins (publico; arquivo PDF fica no Storage)
create table public.documentos (
  id              bigint generated always as identity primary key,
  titulo          text not null,
  descricao       text,
  categoria       text not null
                  check (categoria in ('relatorio_autoavaliacao', 'boletim_informativo')),
  ano_referencia  smallint not null check (ano_referencia between 2000 and 2100),
  storage_path    text not null unique
                  check (lower(storage_path) like '%.pdf'),
  created_by      uuid default auth.uid() references public.usuarios (id) on delete set null,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create index documentos_ano_categoria_idx
  on public.documentos (ano_referencia desc, categoria);

-- -----------------------------------------------------------------------------
-- 5. Triggers
-- -----------------------------------------------------------------------------

create trigger usuarios_set_updated_at    before update on public.usuarios
  for each row execute function public.set_updated_at();
create trigger dashboards_set_updated_at  before update on public.dashboards
  for each row execute function public.set_updated_at();
create trigger devolutivas_set_updated_at before update on public.devolutivas
  for each row execute function public.set_updated_at();
create trigger documentos_set_updated_at  before update on public.documentos
  for each row execute function public.set_updated_at();

-- Todo novo cadastro no Auth vira "aluno". O perfil NUNCA e lido de
-- raw_user_meta_data (controlado pelo cliente => escalada de privilegio).
-- Promocao a outros perfis e feita somente por um admin.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.usuarios (id, nome, email, perfil_id)
  select
    new.id,
    coalesce(nullif(new.raw_user_meta_data ->> 'nome', ''), split_part(new.email, '@', 1)),
    new.email,
    p.id
  from public.perfis p
  where p.codigo = 'aluno';
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- -----------------------------------------------------------------------------
-- 6. Row Level Security
-- -----------------------------------------------------------------------------

alter table public.perfis            enable row level security;
alter table public.usuarios          enable row level security;
alter table public.dashboards        enable row level security;
alter table public.dashboard_perfis  enable row level security;
alter table public.devolutivas       enable row level security;
alter table public.documentos        enable row level security;

-- Defesa em profundidade: visitante anonimo nao toca em dados restritos.
revoke all on public.usuarios, public.dashboards, public.dashboard_perfis from anon;

-- perfis: leitura para logados (nao ha escrita pela API)
create policy perfis_select on public.perfis
  for select to authenticated using (true);

-- usuarios: cada um le a propria linha; admin le/atualiza todas.
-- Sem policy de UPDATE para o proprio usuario (evita auto-promocao).
-- INSERT so ocorre via trigger handle_new_user; DELETE via cascade do Auth.
create policy usuarios_select on public.usuarios
  for select to authenticated
  using (id = auth.uid() or public.is_admin());

create policy usuarios_update_admin on public.usuarios
  for update to authenticated
  using (public.is_admin())
  with check (public.is_admin());

-- dashboards: anon nada. Logado ve se admin (todos), ou se ativo e
-- (avaliador_mec OU perfil vinculado em dashboard_perfis).
create policy dashboards_select on public.dashboards
  for select to authenticated
  using (
    public.is_admin()
    or (
      ativo
      and (
        public.perfil_atual() = 'avaliador_mec'
        or exists (
          select 1
          from public.dashboard_perfis dp
          join public.perfis p on p.id = dp.perfil_id
          where dp.dashboard_id = dashboards.id
            and p.codigo = public.perfil_atual()
        )
      )
    )
  );

create policy dashboards_admin_write on public.dashboards
  for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

create policy dashboard_perfis_admin on public.dashboard_perfis
  for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

-- devolutivas: leitura publica (RN01); escrita so admin
create policy devolutivas_select on public.devolutivas
  for select to anon, authenticated using (true);

create policy devolutivas_admin_write on public.devolutivas
  for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

-- documentos: leitura publica (RN01); escrita so admin
create policy documentos_select on public.documentos
  for select to anon, authenticated using (true);

create policy documentos_admin_write on public.documentos
  for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

-- -----------------------------------------------------------------------------
-- 7. Storage: bucket publico somente PDF (RN04)
-- -----------------------------------------------------------------------------

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('documentos', 'documentos', true, 20971520, array['application/pdf'])
on conflict (id) do update
  set public = excluded.public,
      file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

create policy documentos_storage_select on storage.objects
  for select to anon, authenticated
  using (bucket_id = 'documentos');

create policy documentos_storage_insert on storage.objects
  for insert to authenticated
  with check (bucket_id = 'documentos' and public.is_admin());

create policy documentos_storage_update on storage.objects
  for update to authenticated
  using (bucket_id = 'documentos' and public.is_admin())
  with check (bucket_id = 'documentos' and public.is_admin());

create policy documentos_storage_delete on storage.objects
  for delete to authenticated
  using (bucket_id = 'documentos' and public.is_admin());
