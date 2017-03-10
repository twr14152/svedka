drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    title test not null,
    'text' text not null
);

