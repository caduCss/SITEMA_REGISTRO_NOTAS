
from interface.tela_principal import iniciar_sistema
from database.conexao import criar_tabela


if __name__ == "__main__":
    # Cria a tabela caso ela ainda não exista
    criar_tabela()

    # Inicia a interface gráfica
    iniciar_sistema()
