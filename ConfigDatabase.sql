create database if not exists quiz;
use quiz;
create table if not exists roles(
    id int auto_increment primary key,
    title varchar(50)
);
create table if not exists users(
    id int auto_increment primary key,
    full_name varchar(255) not null,
    age int,
    phone varchar(15) not null,
    password varchar(255) not null,
    role_id int,
    register_date timestamp default current_timestamp,
    foreign key (role_id) references roles(id)
);
create table if not exists questions(
    id int auto_increment primary key,
    title varchar(255) not null,
    opa varchar(255) not null,
    opb varchar(255) not null,
    opc varchar(255) not null,
    opd varchar(255) not null,
    correct_answer enum('opa', 'opb', 'opc', 'opd') not null
);
create table if not exists user_rank(
    id int auto_increment primary key,
    user_id int,
    score int not null,
    rank int not null,
    foreign key (user_id) references users(id)
);
insert into roles(title)
values
('administrator'),
('participant');
insert into users(full_name, phone, password, role_id)
values
('Vahid Mohammadi', '09999999999', 'admin123', 1);