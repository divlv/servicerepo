-- ### Already created/granted by Dockerized PostgreSQL ###
-- create database servicerepo;
-- create user sreapp with encrypted password 'scheme54inverse63Frenzy';
-- grant all privileges on database servicerepo to sreapp;

DROP TABLE if exists service_repo;
CREATE TABLE service_repo( 
    id BIGSERIAL,
    endpoint varchar(254),
    servicename varchar(254),
    queryvars jsonb,
    method varchar(10),
    area varchar(32),
    tags jsonb,
    incomingjson jsonb,
    outgoingjson jsonb,
    description varchar(254),
    deleted int DEFAULT 0 NOT NULL,   
    insdat timestamp DEFAULT now() NOT NULL
);
