-- =============================================================================
-- Dashboards oficiais da CPA (Looker Studio / Google Data Studio).
--
-- Substitui os 3 dashboards de demonstração (DASH-01..03) pelos 4 relatórios
-- enviados pela CPA, separados por público respondente. Os dados dos relatórios
-- são fictícios, com a mesma estrutura da pesquisa real; quando a CPA trocar a
-- base, os links continuam os mesmos.
--
-- Visibilidade (RN02, RN03):
--   * Aluno: relatórios de Aluno(a) Presencial e Aluno(a) EAD.
--   * Coordenador: os 4 relatórios.
--   * Avaliador MEC e Admin: todos os ativos, por regra da RLS (sem vínculo).
--
-- Os relatórios só abrem para contas Google do domínio Impacta: a permissão do
-- Looker Studio é independente do login do portal.
-- =============================================================================

insert into public.dashboards (codigo, nome, descricao, url_embed, ordem, ativo) values
  ('DASH-01', 'Pesquisa CPA — Aluno(a) Presencial',
   'Resultados da pesquisa de avaliação institucional respondida pelos alunos dos cursos presenciais.',
   'https://datastudio.google.com/embed/reporting/c6fac40f-46c9-489d-a63f-653537ca5719/page/p_k1tjc7bebd', 1, true),
  ('DASH-02', 'Pesquisa CPA — Aluno(a) EAD',
   'Resultados da pesquisa de avaliação institucional respondida pelos alunos dos cursos a distância.',
   'https://datastudio.google.com/embed/reporting/a29dac9a-c940-4eec-9d63-7d811debf2ec/page/p_k1tjc7bebd', 2, true),
  ('DASH-03', 'Pesquisa CPA — Professores',
   'Resultados da pesquisa de avaliação institucional respondida pelo corpo docente.',
   'https://datastudio.google.com/embed/reporting/ee6a7999-c41a-41e7-9c73-2ac0fff59d49/page/p_k1tjc7bebd', 3, true),
  ('DASH-04', 'Pesquisa CPA — Corpo Técnico Administrativo',
   'Resultados da pesquisa de avaliação institucional respondida pelos colaboradores técnico-administrativos.',
   'https://datastudio.google.com/embed/reporting/d1cfe171-e39a-47bd-abc1-c131be08d632/page/p_k1tjc7bebd', 4, true)
on conflict (codigo) do update set
  nome       = excluded.nome,
  descricao  = excluded.descricao,
  url_embed  = excluded.url_embed,
  ordem      = excluded.ordem,
  ativo      = excluded.ativo,
  updated_at = now();

-- Refaz os vínculos desses 4 dashboards (outros dashboards não são alterados).
delete from public.dashboard_perfis
 where dashboard_id in (
   select id from public.dashboards where codigo in ('DASH-01', 'DASH-02', 'DASH-03', 'DASH-04')
 );

insert into public.dashboard_perfis (dashboard_id, perfil_id)
select d.id, p.id
from (values
  ('DASH-01', 'aluno'),
  ('DASH-01', 'coordenador'),
  ('DASH-02', 'aluno'),
  ('DASH-02', 'coordenador'),
  ('DASH-03', 'coordenador'),
  ('DASH-04', 'coordenador')
) as v (dash, perfil)
join public.dashboards d on d.codigo = v.dash
join public.perfis p on p.codigo = v.perfil
on conflict do nothing;
