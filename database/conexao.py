import sqlite3

# Define o caminho do banco de dados
CAMINHO_BANCO = "database/sistema_notas.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    return conexao


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DROP TABLE IF EXISTS alunos")

    cursor.execute("""
        CREATE TABLE alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            simulado1 NUMERIC,
            simulado2 NUMERIC,
            av NUMERIC,
            avs NUMERIC,
            nota_final NUMERIC
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()

    print("Tabela de alunos recriada com sucesso!")
