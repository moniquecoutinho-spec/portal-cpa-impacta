-- =============================================================================
-- Testes das regras de acesso (pgTAP). Executar com: supabase test db
-- Tudo roda dentro de uma transação e é desfeito no final (rollback).
-- =============================================================================

begin;
select plan(11);

-- -----------------------------------------------------------------------------
-- Estrutura e dashboards oficiais
-- -----------------------------------------------------------------------------
select is((select count(*)::int from public.perfis), 4,
  'existem 4 perfis cadastrados');

select is((select count(*)::int from public.dashboards), 4,
  'existem os 4 dashboards oficiais (DASH-01..04)');

-- -----------------------------------------------------------------------------
-- Cadastro: sempre nasce aluno, mesmo que o cliente tente enviar outro perfil
-- -----------------------------------------------------------------------------
insert into auth.users (id, email, raw_user_meta_data)
values (
  '11111111-1111-1111-1111-111111111111',
  'usuario.teste@exemplo.com',
  '{"nome": "Usuario Teste", "perfil": "admin"}'
);

select is(
  (select p.codigo from public.usuarios u
     join public.perfis p on p.id = u.perfil_id
    where u.id = '11111111-1111-1111-1111-111111111111'),
  'aluno',
  'novo cadastro vira aluno e ignora o perfil enviado pelo cliente');

-- -----------------------------------------------------------------------------
-- Visitante (anon)
-- -----------------------------------------------------------------------------
set local role anon;

select throws_ok('select * from public.dashboards', '42501', null,
  'visitante não acessa dashboards');
select lives_ok('select * from public.devolutivas',
  'visitante lê o mural de devolutivas (RN01)');
select lives_ok('select * from public.documentos',
  'visitante lê relatórios e boletins (RN01)');

reset role;

-- -----------------------------------------------------------------------------
-- Aluno
-- -----------------------------------------------------------------------------
set local request.jwt.claim.sub = '11111111-1111-1111-1111-111111111111';
set local role authenticated;

select is((select count(*)::int from public.dashboards), 2,
  'aluno vê só os relatórios de alunos, DASH-01 e DASH-02 (RN02)');
select is((select count(*)::int from public.dashboards where codigo in ('DASH-03', 'DASH-04')), 0,
  'aluno não vê os relatórios de professores e corpo técnico (RN02)');

-- tentativa de autopromoção: não há policy de UPDATE para o próprio usuário
update public.usuarios
   set perfil_id = (select id from public.perfis where codigo = 'admin')
 where id = auth.uid();

reset role;

select is(
  (select p.codigo from public.usuarios u
     join public.perfis p on p.id = u.perfil_id
    where u.id = '11111111-1111-1111-1111-111111111111'),
  'aluno',
  'aluno não consegue se autopromover a admin');

-- -----------------------------------------------------------------------------
-- Coordenador
-- -----------------------------------------------------------------------------
update public.usuarios
   set perfil_id = (select id from public.perfis where codigo = 'coordenador')
 where id = '11111111-1111-1111-1111-111111111111';

set local role authenticated;
select is((select count(*)::int from public.dashboards), 4,
  'coordenador vê os 4 dashboards');
reset role;

-- -----------------------------------------------------------------------------
-- Avaliador MEC: vê todos os dashboards ATIVOS
-- -----------------------------------------------------------------------------
update public.usuarios
   set perfil_id = (select id from public.perfis where codigo = 'avaliador_mec')
 where id = '11111111-1111-1111-1111-111111111111';
update public.dashboards set ativo = false where codigo = 'DASH-04';

set local role authenticated;
select is((select count(*)::int from public.dashboards), 3,
  'avaliador MEC vê todos os dashboards ativos e nenhum inativo (RN03)');
reset role;

select * from finish();
rollback;
