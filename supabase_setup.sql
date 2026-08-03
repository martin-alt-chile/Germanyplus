-- Germany+ · persistencia para una sola usuaria (Lula)
-- Ejecuta TODO este archivo una sola vez en Supabase > SQL Editor.

create table if not exists public.germany_plus_state (
    user_id text primary key,
    state jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now(),
    constraint germany_plus_state_is_object
      check (jsonb_typeof(state) = 'object')
);

comment on table public.germany_plus_state is
  'Estado completo de Germany+; una fila JSON por perfil.';

alter table public.germany_plus_state enable row level security;

-- Germany+ se conecta desde el servidor de Streamlit usando una Secret key
-- (sb_secret_...) o, en proyectos antiguos, service_role. Ambas son claves
-- de servidor y omiten RLS. No deben publicarse ni quedar en GitHub.
revoke all on table public.germany_plus_state from anon, authenticated;
grant select, insert, update, delete on table public.germany_plus_state to service_role;

insert into public.germany_plus_state (user_id, state)
values (
    'lula',
    '{
      "version": 2,
      "xp": 0,
      "sessions": [],
      "vocabulary": {},
      "preferences": {
        "show_spanish_help": true,
        "daily_goal": 1
      }
    }'::jsonb
)
on conflict (user_id) do nothing;

-- Comprobación final: debe devolver una fila llamada lula.
select user_id, updated_at, jsonb_typeof(state) as state_type
from public.germany_plus_state
where user_id = 'lula';
