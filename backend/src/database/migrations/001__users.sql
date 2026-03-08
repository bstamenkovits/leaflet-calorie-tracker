create table public.users (
    id text not null,
    name text not null,
    constraint users_pkey primary key (id)
) TABLESPACE pg_default;
