create database %s
  with owner = %s
       encoding = 'UTF8'
       tablespace = pg_default
       connection limit = -1;

create table books (
	id          serial,

	classname   varchar(200),
	name        varchar(200),

	subject     varchar(200),
	author      varchar(200),
	publish     varchar(200),

	amount      integer,
	offed       integer,
	cost        float,

	constraint pk_book    primary key (id)
);

create table gettings  (
	get_id  serial,

	id      integer,
	year    integer,
	num     integer,
	price   float,

	constraint pk_getting primary key (get_id),
	constraint fk_book    foreign key (id) references books (id)
);

create table offings  (
	off_id  serial,

	id      integer,
	year    integer,
	num     integer,

	constraint pk_offing primary key (off_id),
	constraint fk_book   foreign key (id) references books (id)
);

create table statics (
	amount_books  integer primary key,
	amount_copies integer,
	amount_cost   float
)
