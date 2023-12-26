create table if not exists alembic_version
(
    version_num varchar(32) not null
        constraint alembic_version_pkc
            primary key
);

alter table alembic_version
    owner to postgres;

create table if not exists users
(
    id       serial
        primary key,
    username varchar(64)  not null
        unique,
    password varchar(255) not null
);

alter table users
    owner to postgres;

create table if not exists hards
(
    id   serial
        primary key,
    name varchar(32) not null
        unique
);

alter table hards
    owner to postgres;

create table if not exists horrors
(
    id   serial
        primary key,
    name varchar(32) not null
        unique
);

alter table horrors
    owner to postgres;

create table if not exists quests
(
    id           serial
        primary key,
    name         varchar(64)        not null,
    slug         varchar(64)        not null
        unique,
    description  varchar(64)        not null,
    legend       text    default 'Здесь может быть ваша легенда'::text,
    files        json,
    price        integer default 0,
    min_players  integer default 1  not null,
    max_players  integer default 1  not null,
    count_actors integer default 1  not null,
    is_hide      boolean default true,
    horror_id    integer            not null
        constraint fk_horror_id
            references horrors,
    hard_id      integer            not null
        constraint fk_hard_id
            references hards,
    play_time    integer default 60 not null,
    age_limit    integer default 18,
    my_erp_id    integer
);

alter table quests
    owner to postgres;

create table if not exists schedules
(
    id       serial
        primary key,
    date     timestamp,
    quest_id integer
        constraint fk_quest_id5
            references quests,
    is_busy  boolean default false
);

alter table schedules
    owner to postgres;

create table if not exists visitors
(
    id    serial
        primary key,
    name  varchar(64) not null,
    email varchar(64),
    phone varchar(15) not null,
    age   integer default 18
);

alter table visitors
    owner to postgres;

create table if not exists orders
(
    id           serial
        primary key,
    visitor_id   integer not null,
    quest_id     integer not null,
    pick_players integer default 1,
    pick_actors  integer default 1,
    pick_hard    integer default 1
        constraint fk_hard_iddqw
            references hards,
    pick_horror  integer default 1
        constraint fk_horror_idddsas
            references horrors,
    pick_date_id integer not null
        constraint fk_pick_date_idd
            references schedules
);

alter table orders
    owner to postgres;

create table if not exists reviews
(
    id       serial
        primary key,
    visitor  text        not null,
    message  varchar(64) not null,
    stars    text default '1'::text,
    quest_id integer
        constraint fk_review_idd1
            references quests
);

alter table reviews
    owner to postgres;

create table if not exists services
(
    id       serial
        primary key,
    name     varchar(64) not null,
    text     text        not null,
    price    integer default 0,
    quest_id integer
        constraint fk_quest_idddd2
            references quests
);

alter table services
    owner to postgres;

create table if not exists order_to_service
(
    id         serial
        primary key,
    order_id   integer not null
        constraint fk_order_iddd4
            references orders,
    service_id integer not null
        constraint fk_service_iddd3
            references services
);

alter table order_to_service
    owner to postgres;

create table if not exists gallery
(
    id       serial
        primary key,
    quest_id integer
        constraint fk_gallery_to_quest_id
            references quests,
    photo    text,
    is_main  boolean
);

alter table gallery
    owner to postgres;

