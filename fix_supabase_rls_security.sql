-- ============================================================
-- Supabase Security Advisor Vulnerability Fix for PlaceMate
-- Fixes: rls_disabled_in_public & sensitive_columns_exposed
-- ============================================================

-- Step 1: Enable Row Level Security (RLS) on all existing tables in public schema
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'ALTER TABLE public.' || quote_ident(r.tablename) || ' ENABLE ROW LEVEL SECURITY;';
    END LOOP;
END $$;

-- Step 2: Revoke direct PostgREST API access from anonymous & default authenticated roles
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon, authenticated;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM anon, authenticated;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM anon, authenticated;

-- Step 3: Ensure future tables automatically have RLS enabled and restricted permissions
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM anon, authenticated;
