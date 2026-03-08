create table public.meals (
    id text not null,
    name text not null,
    constraint meals_pkey primary key (id)
) TABLESPACE pg_default;
