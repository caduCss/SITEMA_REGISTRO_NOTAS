CREATE DATABASE sistema_notas;                          -- Cria o banco de dados do zero com o nome escolhido

\c sistema_notas;                                       -- Comando do terminal PostgreSQL para entrar nesse banco criado

-- -------------------------------------------------------------------------
-- FAXINA E CRIAÇÃO DA TABELA ATUALIZADA
-- -------------------------------------------------------------------------

DROP TABLE IF EXISTS alunos;                            -- Apaga a tabela antiga se ela existir para evitar conflitos

CREATE TABLE alunos (                                   -- Inicia o desenho da estrutura da tabela de alunos
    id SERIAL PRIMARY KEY,                              -- Cria um ID numérico que aumenta sozinho e nunca se repete
    nome VARCHAR(100) NOT NULL,                         -- Campo de texto de até 100 letras, obrigatório preencher
    matricula VARCHAR(20) UNIQUE NOT NULL,              -- Matrícula obrigatória e que bloqueia números duplicados
    simulado1 NUMERIC(4, 2),                            -- Nota com até 4 dígitos (ex: 10.00), aceitando ficar vazia
    simulado2 NUMERIC(4, 2),                            -- Segundo simulado, também aceita valor nulo (vazio)
    av NUMERIC(4, 2),                                   -- Campo da prova oficial (AV), sem obrigatoriedade de nota
    avs NUMERIC(4, 2),                                  -- Coluna da recuperação (AVS), aceita nulo se passar direto
    nota_final NUMERIC(4, 2)                            -- Guarda a média calculada ou digitada pelo professor
);                                                      -- Fecha a configuração da tabela de forma segura