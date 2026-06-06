from database.conexao import conectar  # Importa a função de conexão com o PostgreSQL

def inserir_aluno(nome, matricula, simulado1, simulado2, av, avs, nota_final):
    """
    Insere um novo aluno no banco de dados. 
    Aceita campos de notas vazios (None), exigindo obrigatoriamente apenas nome e matrícula.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    comando = """
        INSERT INTO alunos (nome, matricula, simulado1, simulado2, av, avs, nota_final)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    
    # Se os campos na interface vierem vazios (''), o Python os trata e envia como None (NULL no banco)
    dados = (
        nome, 
        matricula, 
        None if str(simulado1).strip() == "" else simulado1,
        None if str(simulado2).strip() == "" else simulado2,
        None if str(av).strip() == "" else av,
        None if str(avs).strip() == "" else avs,
        None if str(nota_final).strip() == "" else nota_final
    )

    try:
        cursor.execute(comando, dados)
        conexao.commit()
    except Exception as erro:
        print(f"Erro ao inserir aluno: {erro}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()


def listar_alunos():
    """
    Busca todos os alunos cadastrados no banco de dados, ordenando-os pelo ID.
    Retorna uma lista de tuplas com os dados de cada aluno.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    comando = "SELECT id, nome, matricula, simulado1, simulado2, av, avs, nota_final FROM alunos ORDER BY id;"
    alunos = []

    try:
        cursor.execute(comando)
        alunos = cursor.fetchall()  # Captura todos os registros retornados pelo SELECT
    except Exception as erro:
        print(f"Erro ao listar alunos: {erro}")
    finally:
        cursor.close()
        conexao.close()
        
    return alunos


def deletar_aluno(matricula):
    """
    Remove um aluno do banco de dados utilizando a matrícula como chave de busca segura.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    comando = "DELETE FROM alunos WHERE matricula = %s;"

    try:
        cursor.execute(comando, (matricula,))
        conexao.commit()
    except Exception as erro:
        print(f"Erro ao deletar aluno: {erro}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()


def atualizar_aluno(nome, matricula, simulado1, simulado2, av, avs, nota_final):
    """
    Atualiza as notas e o nome de um aluno utilizando a matrícula como chave.
    Garante milimetricamente que cada nota vá para a coluna correta.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    # Mapeamento cirúrgico de cada campo para seu respectivo %s
    comando = """
        UPDATE alunos 
        SET nome = %s, 
            simulado1 = %s, 
            simulado2 = %s, 
            av = %s, 
            avs = %s, 
            nota_final = %s
        WHERE matricula = %s;
    """

    # Tratamento de segurança para notas vazias no UPDATE
    s1_v = None if str(simulado1).strip() == "" else simulado1
    s2_v = None if str(simulado2).strip() == "" else simulado2
    av_v = None if str(av).strip() == "" else av
    avs_v = None if str(avs).strip() == "" else avs
    nf_v = None if str(nota_final).strip() == "" else nota_final

    # A ordem desta tupla segue exatamente a ordem dos %s no comando SQL acima
    dados = (nome, s1_v, s2_v, av_v, avs_v, nf_v, matricula)

    try:
        cursor.execute(comando, dados)
        conexao.commit()
    except Exception as erro:
        print(f"Erro ao atualizar aluno: {erro}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()