CREATE USER csv WITH PASSWORD 'csv_pw';
CREATE DATABASE csv_db owner csv;
\connect csv_db
CREATE TABLE emails (
    name VARCHAR(255),
    email VARCHAR(320),
    UNIQUE (email)
);
GRANT all privileges ON TABLE emails to csv;
\disconnect
