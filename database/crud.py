# responsavel pela conexão com banco
from database.conexao import conectar

# função recebe dados dos alunos
def inserir_aluno(nome, matricula, nota1, nota2, nota_final):

    conexao = conectar() # abrir a conexão
    cursor = conexao.cursor() # objeto de cursor para interagir com o banco de dados

# insert into -> está inserindo dados na tabela
# values _> são os valores que serão enviados
    comando = """ 
    INSERT INTO alunos
    (nome, matricula, nota1, nota2, nota_final)
    VALUES (%s, %s, %s, %s, %s)
    """
# % -> ão placeholders(espaços reservados) do psycopg2. Eles evitam, concatenação insegura, problemas de formatação
    
    cursor.execute(comando, (nome, matricula, nota1, nota2, nota_final)) # substitui os %, envia para postegresql, executa com segurança

    conexao.commit() # confirma permanentemente a alteração no banco

    print("Aluno cadastrado com sucesso!") # printa na tela.

    cursor.close() # fecha os recurso.
    conexao.close() # fecha os recurso.

# Função responsável por buscar todos os alunos no banco
def listar_alunos():

    # Abre conexão com PostgreSQL
    conexao = conectar()

    # Cria cursor responsável por executar SQL
    cursor = conexao.cursor()

    # Comando SQL para buscar todos os alunos
    comando = "SELECT * FROM alunos"

    # Executa o comando SQL
    cursor.execute(comando)

    # Busca todos os registros retornados pelo SELECT
    alunos = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna os dados para quem chamou a função
    return alunos

# Função responsável por atualizar dados de um aluno
def atualizar_aluno(nome, matricula, nota1, nota2, nota_final):

    # Abre conexão com PostgreSQL
    conexao = conectar()

    # Cria cursor para executar SQL
    cursor = conexao.cursor()

    # Comando SQL de atualização
    comando = """
    UPDATE alunos
    SET nome = %s,
        nota1 = %s,
        nota2 = %s,
        nota_final = %s
    WHERE matricula = %s
    """

    # Executa o UPDATE
    cursor.execute(comando, (nome, nota1, nota2, nota_final, matricula))

    # Confirma alteração no banco
    conexao.commit()

    print("Aluno atualizado com sucesso!")

    # Fecha recursos
    cursor.close()
    conexao.close()

    # Função responsável por remover um aluno do banco
def deletar_aluno(matricula):

    conexao = conectar()
    cursor = conexao.cursor()

    comando = """
    DELETE FROM alunos
    WHERE matricula = %s
    """
    print("Matrícula recebida:", matricula)
    
    cursor.execute(comando, (matricula,))

    conexao.commit()

    print("Aluno removido com sucesso!")

    cursor.close()
    conexao.close()