create table public.servings (
    id text not null,
    name text not null,
    size_g double precision null,
    ingredient_id text null,
    constraint servings_pkey primary key (id),
    constraint servings_ingredient_id_fkey foreign KEY (ingredient_id) references ingredients (id) on update CASCADE on delete CASCADE
) TABLESPACE pg_default;
