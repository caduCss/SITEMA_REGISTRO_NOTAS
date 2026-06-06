import os
import sys
from interface.tela_principal import iniciar_sistema
from database.conexao import conectar

# Força o Python a mapear as pastas internas corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def atualizar_estrutura_banco():
    """
    Função de segurança que atualiza a tabela 'alunos' no PostgreSQL
    para conter os novos campos de notas aceitando valores nulos (vazios).
    """
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        print("Verificando e atualizando a tabela no PostgreSQL...")
        
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
        """)
        
        # Bloco de segurança: Tenta adicionar cada coluna nova. 
        # Se elas já existirem, o banco apenas ignora e não quebra o programa.
        novas_colunas = ["simulado1", "simulado2", "av", "avs"]
        for coluna in novas_colunas:
            try:
                cursor.execute(f"ALTER TABLE alunos ADD COLUMN {coluna} NUMERIC(4, 2);")
                print(f"Coluna '{coluna}' adicionada com sucesso!")
            except Exception:
                # Se der erro aqui, significa que a coluna já existia no banco, então podemos ignorar o aviso
                conexao.rollback() 
                
        conexao.commit()
        cursor.close()
        conexao.close()
        print("Estrutura do banco de dados validada e pronta para aceitar nulos!")
        
    except Exception as e:
        print("Aviso ao validar o banco de dados:", e)

if __name__ == "__main__":
    atualizar_estrutura_banco()  # Executa a validação de colunas antes da tela abrir
    iniciar_sistema()            # Abre a interface gráfica do Tkinter