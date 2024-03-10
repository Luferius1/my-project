Install docker-compose Postgres

Create database myapp in Postgres

CREATE DATABASE myapp;

Create table name "notes"

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
