from database.conexao import conectar


def inserir_aluno(nome, matricula, simulado1, simulado2, av, avs, nota_final):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO alunos (
            nome, matricula, simulado1, simulado2, av, avs, nota_final
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nome, matricula, simulado1, simulado2, av, avs, nota_final))

    conexao.commit()
    cursor.close()
    conexao.close()


def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, matricula, simulado1, simulado2, av, avs, nota_final
        FROM alunos
        ORDER BY id
    """)

    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return alunos


def deletar_aluno(matricula):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM alunos WHERE matricula = ?",
        (matricula,)
    )

    conexao.commit()
    cursor.close()
    conexao.close()


def atualizar_aluno(nome, matricula, simulado1, simulado2, av, avs, nota_final):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE alunos
        SET nome = ?,
            simulado1 = ?,
            simulado2 = ?,
            av = ?,
            avs = ?,
            nota_final = ?
        WHERE matricula = ?
    """, (
        nome, simulado1, simulado2, av, avs, nota_final, matricula
    ))

    conexao.commit()
    cursor.close()
    conexao.close()
