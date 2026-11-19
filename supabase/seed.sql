-- =============================================================================
-- Seed: dashboards de demonstracao (DASH-01..03) e vinculos com perfis.
-- As URLs sao PLACEHOLDERS: o Admin da CPA as substitui pelo painel
-- administrativo quando os links oficiais do Looker Studio forem enviados.
-- Admin e avaliador_mec veem tudo por regra de RLS, entao nao entram aqui.
-- =============================================================================

insert into public.dashboards (codigo, nome, descricao, url_embed, ordem) values
  ('DASH-01', 'Pesquisa Institucional CPA',
   'Satisfacao geral, infraestrutura fisica, laboratorios, biblioteca e atendimento academico.',
   'https://lookerstudio.google.com/embed/reporting/00000000-0000-0000-0000-000000000001/page/demo', 1),
  ('DASH-02', 'Avaliacao Docente por Curso',
   'Didatica, cumprimento do plano de ensino e feedback dos docentes por curso.',
   'https://lookerstudio.google.com/embed/reporting/00000000-0000-0000-0000-000000000002/page/demo', 2),
  ('DASH-03', 'Acompanhamento de Egressos',
   'Empregabilidade, area de atuacao, faixa salarial e continuidade academica dos ex-alunos.',
   'https://lookerstudio.google.com/embed/reporting/00000000-0000-0000-0000-000000000003/page/demo', 3)
on conflict (codigo) do nothing;

insert into public.dashboard_perfis (dashboard_id, perfil_id)
select d.id, p.id
from (values
  ('DASH-01', 'aluno'),
  ('DASH-01', 'coordenador'),
  ('DASH-02', 'coordenador'),
  ('DASH-03', 'coordenador')
) as v (dash, perfil)
join public.dashboards d on d.codigo = v.dash
join public.perfis p on p.codigo = v.perfil
on conflict do nothing;
