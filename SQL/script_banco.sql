CREATE DATABASE sistema_notas;

\c sistema_notas;

CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    nota1 NUMERIC(5,2),
    nota2 NUMERIC(5,2),
    nota_final NUMERIC(5,2)
);