create table public.ingredients (
    id text not null,
    name text not null,
    calories_kcal double precision null,
    fat_g double precision null,
    carbs_g double precision null,
    protein_g double precision null,
    type text null,
    constraint ingredients_pkey primary key (id)
) TABLESPACE pg_default;
