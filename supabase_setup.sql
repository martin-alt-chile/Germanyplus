-- Germany+ guarda todo el progreso de Lula en una sola fila JSON.
-- Ejecuta este archivo una sola vez en Supabase > SQL Editor.

create table if not exists public.germany_plus_state (
    user_id text primary key,
    state jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now()
);

alter table public.germany_plus_state enable row level security;

-- La app usa la service role key solamente desde el servidor de Streamlit.
-- Esa clave omite RLS; no debe aparecer en GitHub ni en el navegador.
revoke all on public.germany_plus_state from anon, authenticated;
grant select, insert, update, delete on public.germany_plus_state to service_role;

insert into public.germany_plus_state (user_id, state)
values (
    'lula',
    '{
      "version": 1,
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
