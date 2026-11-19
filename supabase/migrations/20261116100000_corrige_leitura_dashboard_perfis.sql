-- =============================================================================
-- Correção: leitura de dashboard_perfis por usuários autenticados
--
-- A policy dashboards_select consulta dashboard_perfis para saber quais perfis
-- acessam cada dashboard. Como essa tabela só tinha policy para admin, o RLS
-- escondia os vínculos de aluno e coordenador, e eles não viam nenhum
-- dashboard (detectado pelos testes em supabase/tests/rls_test.sql).
--
-- Cada usuário passa a ler apenas os vínculos do PRÓPRIO perfil, sem revelar
-- dashboards destinados a outros perfis (RN02).
-- =============================================================================

create policy dashboard_perfis_select_proprio on public.dashboard_perfis
  for select to authenticated
  using (
    perfil_id = (
      select p.id
      from public.perfis p
      where p.codigo = public.perfil_atual()
    )
  );
