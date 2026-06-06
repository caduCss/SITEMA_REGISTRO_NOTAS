from database.conexao import conectar                # Puxa o nosso "abridor de portas" do banco de dados

def inserir_aluno(nome, matricula, simulado1, simulado2, av, avs, nota_final):
    conexao = conectar()                              # Abre a conexão com o PostgreSQL
    cursor = conexao.cursor()                         # Pega o "cursor", que é quem vai escrever o comando SQL

    comando = """
        INSERT INTO alunos (nome, matricula, simulado1, simulado2, av, avs, nota_final)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """                                               # Prepara o modelo do comando de inserção
    
    dados = (
        nome,                                         # O nome vai no primeiro %s
        matricula,                                    # A matrícula no segundo
        None if str(simulado1).strip() == "" else simulado1,  # Se o simulado1 tiver vazio, grava como NULL no banco
        None if str(simulado2).strip() == "" else simulado2,  # Faz o mesmo com o simulado2
        None if str(av).strip() == "" else av,        # Se não tiver nota de AV, o banco aceita como nulo
        None if str(avs).strip() == "" else avs,      # AVS nula caso o aluno não tenha feito recuperação
        None if str(nota_final).strip() == "" else nota_final # Nota final vazia se ele ainda estiver de REC
    )                                                 # Essa tupla garante que os dados entrem na ordem certa

    try:
        cursor.execute(comando, dados)                # Tenta rodar o comando com os dados tratados
        conexao.commit()                              # Se deu certo, salva as alterações definitivamente
    except Exception as erro:                         # Se o banco reclamar de algo (tipo matrícula repetida)
        print(f"Erro ao inserir aluno: {erro}")       # Mostra o erro no terminal pra gente debugar
        conexao.rollback()                            # Volta atrás pra não deixar o banco em estado estranho
    finally:
        cursor.close()                                # Fecha o cursor pra liberar recursos
        conexao.close()                               # Fecha a conexão pra não deixar "pendurada"


def listar_alunos():
    conexao = conectar()                              # Abre o portão do banco novamente
    cursor = conexao.cursor()                         # Pega o cursor pra fazer a consulta

    comando = "SELECT id, nome, matricula, simulado1, simulado2, av, avs, nota_final FROM alunos ORDER BY id;"
    alunos = []                                       # Cria uma lista vazia pra guardar o que vier do banco

    try:
        cursor.execute(comando)                       # Executa o SELECT pra buscar todo mundo
        alunos = cursor.fetchall()                    # Puxa todos os registros e joga dentro da nossa lista
    except Exception as erro:                         # Caso a tabela não exista ou o SELECT falhe
        print(f"Erro ao listar alunos: {erro}")       # Avisa a gente no terminal
    finally:
        cursor.close()                                # Fecha o cursor por boa prática
        conexao.close()                               # Fecha a conexão pra economizar energia do servidor
        
    return alunos                                     # Devolve a lista de alunos (ou vazia) pro Python usar


def deletar_aluno(matricula):
    conexao = conectar()                              # Conecta no banco pra poder apagar
    cursor = conexao.cursor()                         # Prepara o cursor

    comando = "DELETE FROM alunos WHERE matricula = %s;" # Comando focado em apagar pela matrícula (que é única)

    try:
        cursor.execute(comando, (matricula,))         # Tenta apagar o aluno que tem essa matrícula
        conexao.commit()                              # Confirma a exclusão de vez
    except Exception as erro:                         # Se algo impedir a deleção
        print(f"Erro ao deletar aluno: {erro}")       # Solta o erro no terminal
        conexao.rollback()                            # Cancela a tentativa pra manter o banco seguro
    finally:
        cursor.close()                                # Fecha o cursor
        conexao.close()                               # Fecha a conexão


def atualizar_aluno(nome, matricula, simulado1, simulado2, av, avs, nota_final):
    conexao = conectar()                              # Abre a conexão pra fazer o UPDATE
    cursor = conexao.cursor()                         # Pega o cursor pra escrever a atualização

    comando = """
        UPDATE alunos 
        SET nome = %s, 
            simulado1 = %s, 
            simulado2 = %s, 
            av = %s, 
            avs = %s, 
            nota_final = %s
        WHERE matricula = %s;
    """                                               # Monta o UPDATE: troca os valores onde a matrícula bater

    # Tratamento para o UPDATE aceitar campos vazios como NULL no banco
    s1_v = None if str(simulado1).strip() == "" else simulado1
    s2_v = None if str(simulado2).strip() == "" else simulado2
    av_v = None if str(av).strip() == "" else av
    avs_v = None if str(avs).strip() == "" else avs
    nf_v = None if str(nota_final).strip() == "" else nota_final

    # A ordem aqui embaixo tem que ser IGUAL aos %s do comando UPDATE lá de cima
    dados = (nome, s1_v, s2_v, av_v, avs_v, nf_v, matricula) # A matrícula vai por último por causa do WHERE

    try:
        cursor.execute(comando, dados)                # Manda o banco atualizar o registro do aluno
        conexao.commit()                              # Se o banco aceitou, salva a mudança
    except Exception as erro:                         # Se houver erro de tipo (como o erro de texto em número)
        print(f"Erro ao atualizar aluno: {erro}")     # Avisa o que aconteceu no terminal
        conexao.rollback()                            # Desfaz a alteração pra não corromper o aluno
    finally:
        cursor.close()                                # Fecha o cursor
        conexao.close()                               # Fecha a conexão com o PostgreSQL