create database ctfsd;

use ctfsd;

create table paint_job (
    id int NOT NULL,
    color varchar(100) NOT NULL,
    painted_time TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);