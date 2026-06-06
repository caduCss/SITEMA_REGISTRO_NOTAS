CREATE DATABASE sistema_notas;

\c sistema_notas;
-- 1. Apaga a tabela antiga com a estrutura velha
DROP TABLE alunos;

-- 2. Cria a tabela nova com suporte a nulos e todas as colunas
CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    simulado1 NUMERIC(4, 2),              
    simulado2 NUMERIC(4, 2),              
    av NUMERIC(4, 2),                     
    avs NUMERIC(4, 2),                    
    nota_final NUMERIC(4, 2)              
);
