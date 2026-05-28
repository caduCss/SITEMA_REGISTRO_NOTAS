import psycopg2

def conectar():
    
    try: 
        # Tentando estabelecer a conexão através do método connect
        conexao = psycopg2.connect(
            host="localhost",                       # Endereço do servidor (geralmente localhost se estiver na sua máquina)
            database="Sistema_Registro_Notas",      # Nome do banco de dados que você criou
            user="postgres",                        # Seu usuário do PostgreSQL (padrão é 'postgres')
            password="20206",                       # A senha que você definiu na instalação do PostgreSQL
            port="5432"                             # Porta padrão do PostgreSQL
        )
        
        print("Conexão realizada com sucesso!")
        
        return conexao
    
    except Exception as erro:
        print("Erro ao conectar:", erro)


