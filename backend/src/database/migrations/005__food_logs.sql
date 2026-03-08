create table public.food_logs (
    id text not null,
    date_added timestamp with time zone not null,
    meal_id text null,
    ingredient_id text null,
    serving_id text null,
    quantity double precision not null,
    user_id text null,
    constraint food_log_pkey primary key (id),
    constraint food_log_id_key unique (id),
    constraint food_logs_ingredient_id_fkey foreign KEY (ingredient_id) references ingredients (id) on update CASCADE on delete CASCADE,
    constraint food_logs_meal_id_fkey foreign KEY (meal_id) references meals (id) on update CASCADE on delete CASCADE,
    constraint food_logs_serving_id_fkey foreign KEY (serving_id) references servings (id) on update CASCADE on delete CASCADE,
    constraint food_logs_user_id_fkey foreign KEY (user_id) references users (id) on update CASCADE on delete CASCADE
) TABLESPACE pg_default;
