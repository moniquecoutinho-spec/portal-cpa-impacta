-- =============================================================================
-- Seed (carga inicial para o banco local e para o CI).
--
-- Os dashboards oficiais e seus vínculos com perfis ficam na migration
-- 20261119000000_dashboards_oficiais.sql, para valerem também em produção.
-- Contas de usuário não ficam aqui: use `python -m scripts.criar_usuarios_teste`.
--
-- Devolutivas abaixo são exemplos fictícios para popular o mural público.
-- O script é reexecutável: não duplica uma devolutiva que já existe (mesmo título).
-- Para popular o banco remoto, cole este trecho no SQL Editor do Supabase:
-- `supabase db push` aplica só migrations e não roda o seed.
-- =============================================================================

insert into public.devolutivas (titulo, area_responsavel, acao, status, data_publicacao)
select v.titulo, v.area_responsavel, v.acao, v.status, v.data_publicacao::date
from (values
  ('Wi-Fi instável nos laboratórios de informática', 'Tecnologia da Informação',
   'Troca dos pontos de acesso dos laboratórios e ampliação do link de internet do campus.',
   'concluido', '2026-03-10'),
  ('Acervo da biblioteca desatualizado', 'Biblioteca',
   'Aquisição de novos títulos das bibliografias básicas e assinatura de uma base de periódicos digitais.',
   'em_andamento', '2026-04-22'),
  ('Dificuldade para agendar atendimento na secretaria', 'Secretaria Acadêmica',
   'Implantação de agendamento online de atendimento, com confirmação por e-mail.',
   'em_andamento', '2026-05-15'),
  ('Poucas opções de alimentação no intervalo', 'Administração',
   'Abertura de processo para ampliar o número de pontos de alimentação e incluir opções mais variadas.',
   'planejado', '2026-06-03'),
  ('Falta de divulgação dos resultados da pesquisa da CPA', 'CPA',
   'Criação do mural de devolutivas e do boletim informativo semestral, ambos públicos.',
   'concluido', '2026-06-18'),
  ('Ar-condicionado com falhas em salas de aula', 'Infraestrutura',
   'Manutenção preventiva em todas as salas e cronograma de substituição dos equipamentos mais antigos.',
   'planejado', '2026-08-07'),
  ('Conteúdo das disciplinas EAD pouco atualizado', 'Coordenação de EAD',
   'Revisão do material das disciplinas com maior número de reclamações, com apoio dos professores responsáveis.',
   'em_andamento', '2026-09-14')
) as v (titulo, area_responsavel, acao, status, data_publicacao)
where not exists (
  select 1 from public.devolutivas d where d.titulo = v.titulo
);
