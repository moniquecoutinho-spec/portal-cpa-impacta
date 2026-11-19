-- =============================================================================
-- Avaliações (ciclos avaliativos) e participação dos alunos.
-- Usadas pelo painel do coordenador e pela área do aluno no app Flask.
-- =============================================================================

create table public.avaliacoes (
  id           bigint generated always as identity primary key,
  titulo       text not null check (char_length(titulo) between 1 and 150),
  data_inicio  date not null,
  data_fim     date not null,
  status       text not null default 'Agendada',
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  constraint avaliacoes_periodo_valido check (data_fim >= data_inicio)
);

create index avaliacoes_data_inicio_idx on public.avaliacoes (data_inicio desc);

create trigger avaliacoes_set_updated_at before update on public.avaliacoes
  for each row execute function public.set_updated_at();

create table public.participacoes (
  id            bigint generated always as identity primary key,
  aluno_id      uuid   not null references public.usuarios (id) on delete cascade,
  avaliacao_id  bigint not null references public.avaliacoes (id) on delete cascade,
  respondida    boolean not null default false,
  constraint unico_aluno_avaliacao unique (aluno_id, avaliacao_id)
);

create index participacoes_avaliacao_id_idx on public.participacoes (avaliacao_id);

-- -----------------------------------------------------------------------------
-- RLS: leitura para logados; escrita para admin e coordenador.
-- Aluno vê apenas as próprias participações.
-- -----------------------------------------------------------------------------

alter table public.avaliacoes    enable row level security;
alter table public.participacoes enable row level security;

revoke all on public.avaliacoes, public.participacoes from anon;

create policy avaliacoes_select on public.avaliacoes
  for select to authenticated using (true);

create policy avaliacoes_gestao on public.avaliacoes
  for all to authenticated
  using (public.perfil_atual() in ('admin', 'coordenador'))
  with check (public.perfil_atual() in ('admin', 'coordenador'));

create policy participacoes_select on public.participacoes
  for select to authenticated
  using (
    aluno_id = auth.uid()
    or public.perfil_atual() in ('admin', 'coordenador')
  );

create policy participacoes_gestao on public.participacoes
  for all to authenticated
  using (public.perfil_atual() in ('admin', 'coordenador'))
  with check (public.perfil_atual() in ('admin', 'coordenador'));
