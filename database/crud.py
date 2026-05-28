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

# essa função conecta no db, executa select, busca os resultados e retornas os dados.
def lista_alunos(): 

    conexao = conectar()
    cursor = conexao.cursor()
    comando = "select * FROM alunos" # busca dados. (*) significa que ele vai buscar todas as colunas
    cursor.execute(comando)
    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()
    return alunos