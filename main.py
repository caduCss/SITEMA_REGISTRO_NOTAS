import os                                              # Permite mexer com pastas e caminhos do sistema operacional
import sys                                             # Dá acesso a variáveis e funções do próprio motor do Python
from interface.tela_principal import iniciar_sistema   # Traz a função que desenha a janela que criamos juntos
from database.conexao import conectar                  # Importa o nosso conector oficial do PostgreSQL

# Força o Python a mapear as pastas internas corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Garante que o Python ache os arquivos locais sem se perder

def atualizar_estrutura_banco():
    """
    Função de segurança que atualiza a tabela 'alunos' no PostgreSQL
    para conter os novos campos de notas aceitando valores nulos (vazios).
    """
    try:
        conexao = conectar()                           # Abre a linha de comunicação direta com o banco de dados
        cursor = conexao.cursor()                      # Cria o cursor, que é quem digita os comandos SQL por nós
        
        print("Verificando e atualizando a tabela no PostgreSQL...") # Joga um aviso no terminal para sabermos o que está rolando
        
        # O comando abaixo cria a tabela nova se ela não existir.
        # Caso ela já exista da versão antiga, nós adicionamos as colunas que estão faltando.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                matricula VARCHAR(20) UNIQUE NOT NULL,
                simulado1 NUMERIC(4, 2),
                simulado2 NUMERIC(4, 2),
                av NUMERIC(4, 2),
                avs NUMERIC(4, 2),
                nota_final NUMERIC(4, 2)
            );
        """)                                           # Cria a estrutura do zero se o banco estiver pelado
        
        # Bloco de segurança: Tenta adicionar cada coluna nova. 
        # Se elas já existirem, o banco apenas ignora e não quebra o programa.
        novas_colunas = ["simulado1", "simulado2", "av", "avs", "nota_final"] # Lista tudo o que o banco precisa ter de colunas
        for coluna in novas_colunas:                   # Roda um loop testando uma por uma dessa lista
            try:
                cursor.execute(f"ALTER TABLE alunos ADD COLUMN {coluna} NUMERIC(4, 2);") # Tenta enfiar a coluna na tabela existente
                print(f"Coluna '{coluna}' adicionada com sucesso!") # Mostra no terminal caso a coluna não existisse antes
            except Exception:
                # Se der erro aqui, significa que a coluna já existia no banco, então podemos ignorar o aviso
                conexao.rollback()                     # Desfaz a tentativa que travou para limpar o erro do banco
                
        conexao.commit()                               # Salva todas as alterações que deram certo de forma definitiva
        cursor.close()                                 # Fecha o digitador de comandos para não gastar memória
        conexao.close()                                # Fecha a conexão com o banco de dados por segurança
        print("Estrutura do banco de dados validada e pronta para aceitar nulos!") # Mensagem de sucesso no terminal
        
    except Exception as e:
        print("Aviso ao validar o banco de dados:", e) # Se o banco estiver desligado ou der erro grave, avisa aqui

if __name__ == "__main__":
    atualizar_estrutura_banco()                        # Roda a faxina e checagem do banco antes de mostrar o programa
    iniciar_sistema()                                  # Com o banco garantido, abre a interface gráfica na tela