from database.conexao import conectar                  # Importa a função conectar exatamente do seu arquivo conexao.py
# -------------------------------
# FUNÇÃO: INSERIR NOVO ALUNO (C)
# -------------------------------
def inserir_aluno(nome, matricula, nota1, nota2, nota_final):

    conexao = conectar()                                # Abre a conexão usando a sua função do arquivo conexao.py
    cursor = conexao.cursor()                           # Cria o objeto de cursor para interagir com o banco de dados

    comando = """ 
    INSERT INTO alunos (nome, matricula, nota1, nota2, nota_final)
    VALUES (%s, %s, %s, %s, %s)
    """                                                 # SQL de inserção utilizando placeholders (%s) de segurança

    cursor.execute(comando, (nome, matricula, nota1, nota2, nota_final))  # Injeta os valores reais e executa a query
    conexao.commit()                                    # Confirma permanentemente a alteração no banco de dados

    print("Aluno cadastrado com sucesso!")              # Print informativo no terminal do console
    cursor.close()                                      # Fecha o cursor liberando o recurso manual
    conexao.close()                                     # Fecha a conexão liberando o recurso manual

# -------------------------------
# FUNÇÃO: LISTAR TODOS OS ALUNOS (R)
# -------------------------------
def listar_alunos():

    conexao = conectar()                                # Abre a conexão com o banco de dados PostgreSQL
    cursor = conexao.cursor()                           # Cria o cursor responsável por executar o comando SQL

    comando = "SELECT * FROM alunos"                    # Comando SQL para buscar todos os alunos da tabela

    cursor.execute(comando)                             # Executa a busca direto no banco de dados
    alunos = cursor.fetchall()                          # Busca e armazena todos os registros retornados pelo SELECT

    cursor.close()                                      # Fecha o cursor manualmente
    conexao.close()                                     # Fecha a conexão manualmente
    return alunos                                       # Retorna os dados obtidos para quem chamou a função

# -------------------------------
# FUNÇÃO: ATUALIZAR DADOS (U)
# -------------------------------
def atualizar_aluno(nome, matricula, nota1, nota2, nota_final):

    conexao = conectar()                                # Abre a conexão ativa com o servidor do PostgreSQL
    cursor = conexao.cursor()                           # Cria o cursor para a execução da query de edição

    comando = """
    UPDATE alunos
    SET nome = %s,
        nota1 = %s,
        nota2 = %s,
        nota_final = %s
    WHERE matricula = %s
    """                                                 # Comando SQL de atualização baseado na chave da matrícula

    cursor.execute(comando, (nome, nota1, nota2, nota_final, matricula))  # Executa o UPDATE mapeando as variáveis nos %s
    conexao.commit()                                    # Confirma permanentemente a alteração efetuada no banco

    print("Aluno updated com sucesso!")                 # Imprime aviso de sucesso interno no terminal
    cursor.close()                                      # Libera o objeto do cursor do sistema
    conexao.close()                                     # Libera o objeto da conexão do sistema

# -------------------------------
# FUNÇÃO: DELETAR REGISTRO (D)
# -------------------------------
def deletar_aluno(matricula):

    conexao = conectar()                                # Inicializa a comunicação com o banco de dados
    cursor = conexao.cursor()                           # Instancia o cursor para rodar a remoção do registro

    comando = """
    DELETE FROM alunos
    WHERE matricula = %s
    """                                                 # Comando SQL para remover o aluno através da matrícula
    print("Matrícula recebida:", matricula)             # Exibe a matrícula capturada no terminal para controle

    cursor.execute(comando, (matricula,))               # Executa a exclusão passando o argumento dentro da tupla
    conexao.commit()                                    # Confirma e salva a exclusão permanentemente no banco

    print("Aluno removido com sucesso!")                # Notifica o encerramento da deleção no terminal
    cursor.close()                                      # Fecha o cursor limpando a memória alocada
    conexao.close()                                     # Fecha a conexão com o banco de dados com segurança