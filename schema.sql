drop table if exists items;
create table items(
    id integer primary key autoincrement,
    name char(80) not null,
    abstract text not null,
    filename char(80) not null,
    category integer not null
);

create table comments(
    id integer primary key autoincrement,
    nick char(32) not null,
    text char(1024) not null,
    time datetime not null,
    pas_id integer not null
);

create table categorys(
    id integer primary key autoincrement,
    name char(60) not null
);

insert into categorys (name) values ("分组1");
insert into categorys (name) values ("分组2");
insert into categorys (name) values ("分组3");
