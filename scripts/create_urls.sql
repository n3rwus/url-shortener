create table public.urls (
    id uuid not null default gen_random_uuid (),
    original_url text not null,
    shortened_url text not null,
    clicks integer null default 0,
    created timestamp without time zone null default CURRENT_TIMESTAMP,
    updated timestamp without time zone null default CURRENT_TIMESTAMP,
    valid_until timestamp without time zone null default (CURRENT_TIMESTAMP + '24:00:00'::interval),

    constraint urls_pkey primary key (id),
    constraint urls_original_url_key unique (original_url),
    constraint urls_shortened_url_key unique (shortened_url)
) TABLESPACE pg_default;

create index IF not exists idx_shortened on public.urls using btree (shortened_url) TABLESPACE pg_default;