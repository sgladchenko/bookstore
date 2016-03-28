create table books (
	id          integer primary key autoincrement not null,

	classname   varchar(200),
	name        varchar(200),

	subject     varchar(200),
	author      varchar(200),
	publish     varchar(200),

	amount      integer,
	offed       integer,
	cost        numeric(5,2)

);

create table gettings  (
	get_id  integer primary key autoincrement not null,

	id      integer,
	year    integer,
	num     integer,
	price   numeric(5,2),

	constraint fk_book foreign key (id) references books (id)
);

create table offings  (
	off_id  integer primary key autoincrement not null,

	id      integer,
	year    integer,
	num     integer,

	constraint fk_book foreign key (id) references books (id)
);

create table statics (
	amount_books  integer primary key,
	amount_copies integer,
	amount_cost   numeric(5,2)
);
