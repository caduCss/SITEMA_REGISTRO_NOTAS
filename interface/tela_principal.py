import tkinter as tk                                    # Importa a biblioteca base da interface gráfica
from tkinter import messagebox, ttk                   # Importa caixas de diálogo e elementos visuais avançados
from database.crud import (                            # Importa as quatro funções CRUD desenvolvidas no banco
    inserir_aluno,
    listar_alunos,
    deletar_aluno,
    atualizar_aluno
)

def iniciar_sistema():                                 # Função principal que monta e gerencia a aplicação

    janela = tk.Tk()                                   # Instancia o objeto da janela principal
    janela.title("Sistema de Registro de Notas")       # Define o texto da barra de título
    janela.geometry("800x750")                         # Redimensionado para caber todos os elementos sem cortar

    # -------------------------------
    # FUNÇÕES DE INTERAÇÃO (EVENTOS)
    # -------------------------------

    def cadastrar_aluno():                             # Executada ao clicar no botão "Cadastrar"
        nome = entry_nome.get()                        # Captura o texto do campo Nome
        matricula = entry_matricula.get()              # Captura o texto do campo Matrícula
        nota1 = entry_nota1.get()                      # Captura o texto do campo Nota 1
        nota2 = entry_nota2.get()                      # Captura o texto do campo Nota 2
        nota_final = entry_nota_final.get()            # Captura o texto do campo Nota Final

        inserir_aluno(nome, matricula, nota1, nota2, nota_final)  # Envia os dados capturados para o banco (INSERT)
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")  # Abre balão de confirmação na tela

        entry_nome.delete(0, tk.END)                   # Limpa o texto do campo Nome
        entry_matricula.delete(0, tk.END)              # Limpa o texto do campo Matrícula
        entry_nota1.delete(0, tk.END)                  # Limpa o texto do campo Nota 1
        entry_nota2.delete(0, tk.END)                  # Limpa o texto do campo Nota 2
        entry_nota_final.delete(0, tk.END)             # Limpa o texto do campo Nota Final
    
    def carregar_alunos():                             # Executada ao abrir o app ou atualizar a lista
        for item in tabela.get_children():             # Loop que percorre todas as linhas visuais da Treeview
            tabela.delete(item)                        # Remove a linha para evitar dados duplicados na tela

        alunos = listar_alunos()                       # Busca a lista de tuplas atualizada no banco (SELECT)
        print(alunos)                                  # Exibe a lista no terminal para controle do desenvolvedor
        
        for aluno in alunos:                           # Loop que percorre cada registro retornado do banco
            tabela.insert("", tk.END, values=aluno)    # Insere o registro no final da tabela visual

    def deletar_selected():                            # Executada ao clicar no botão "Deletar"
        item_selecionado = tabela.selection()          # Captura o identificador da linha selecionada na Treeview
        print(item_selecionado)                        # Exibe o id interno do Tkinter no terminal
        
        if not item_selecionado:                       # Valida se o usuário realmente clicou em algo da lista
            messagebox.showwarning("Aviso", "Selecione um aluno para deletar.")  # Avisa que a seleção está vazia
            return                                     # Cancela a execução da função

        dados_aluno = tabela.item(item_selecionado[0]) # Busca o dicionário de dados da linha selecionada
        print(dados_aluno)                             # Exibe os dados da linha no terminal
        
        valores = dados_aluno["values"]                # Extrai a lista de valores (id, nome, matricula...)
        matricula = str(valores[2]).strip()            # Captura a matrícula (índice 2) limpando espaços em branco

        deletar_aluno(matricula)                       # Executa o comando SQL de remoção usando a matrícula (DELETE)
        carregar_alunos()                              # Recarrega a tabela visual para refletir a exclusão
        messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")  # Informa o sucesso ao usuário
        
        entry_nome.delete(0, tk.END)                   # Limpa o campo Nome após deletar o aluno
        entry_matricula.delete(0, tk.END)              # Limpa o campo Matrícula após deletar o aluno
        entry_nota1.delete(0, tk.END)                  # Limpa o campo Nota 1 após deletar o aluno
        entry_nota2.delete(0, tk.END)                  # Limpa o campo Nota 2 após deletar o aluno
        entry_nota_final.delete(0, tk.END)             # Limpa o campo Nota Final após deletar o aluno

    def selecionar_aluno(event):                       # Executada ao dar um clique em uma linha da tabela
        item_selecionado = tabela.selection()          # Identifica qual linha recebeu o clique do mouse

        if not item_selecionado:                       # Valida se há uma linha de fato selecionada
            return                                     # Sai da função caso o clique seja inválido

        dados_aluno = tabela.item(item_selecionado[0]) # Busca os dados da linha clicada
        valores = dados_aluno["values"]                # Extrai a lista com as informações do aluno

        entry_nome.delete(0, tk.END)                   # Limpa o campo de entrada do Nome
        entry_matricula.delete(0, tk.END)              # Limpa o campo de entrada da Matrícula
        entry_nota1.delete(0, tk.END)                  # Limpa o campo de entrada da Nota 1
        entry_nota2.delete(0, tk.END)                  # Limpa o campo de entrada da Nota 2
        entry_nota_final.delete(0, tk.END)             # Limpa o campo de entrada da Nota Final

        entry_nome.insert(0, valores[1])               # Joga o Nome da tabela para dentro do input correspondente
        entry_matricula.insert(0, valores[2])          # Joga a Matrícula da tabela para dentro do input correspondente
        entry_nota1.insert(0, valores[3])              # Joga a Nota 1 da tabela para dentro do input correspondente
        entry_nota2.insert(0, valores[4])              # Joga a Nota 2 da tabela para dentro do input correspondente
        entry_nota_final.insert(0, valores[5])         # Joga a Nota Final da tabela para dentro do input correspondente
    
    def atualizar_dados():                             # Executada ao clicar no botão "Atualizar"
        nome = entry_nome.get()                        # Pega o valor atual editado no campo Nome
        matricula = entry_matricula.get()              # Pega o valor (chave) no campo Matrícula
        nota1 = entry_nota1.get()                      # Pega o valor atual editado no campo Nota 1
        nota2 = entry_nota2.get()                      # Pega o valor atual editado no campo Nota 2
        nota_final = entry_nota_final.get()            # Pega o valor atual editado no campo Nota Final

        atualizar_aluno(nome, matricula, nota1, nota2, nota_final)  # Passa os dados para a query SQL (UPDATE)
        carregar_alunos()                              # Recarrega a tabela com as alterações do banco
        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")  # Alerta visual de sucesso da operação
    
        entry_nome.delete(0, tk.END)                   # Reseta o campo Nome para o padrão vazio
        entry_matricula.delete(0, tk.END)              # Reseta o campo Matrícula para o padrão vazio
        entry_nota1.delete(0, tk.END)                  # Reseta o campo Nota 1 para o padrão vazio
        entry_nota2.delete(0, tk.END)                  # Reseta o campo Nota 2 para o padrão vazio
        entry_nota_final.delete(0, tk.END)             # Reseta o campo Nota Final para o padrão vazio

    # -------------------------------
    # COMPONENTES VISUAIS (WIDGETS)
    # -------------------------------

    titulo = tk.Label(janela, text="Sistema de Registro de Notas", font=("Arial", 18, "bold"))
    titulo.pack(pady=20)                               # Renderiza o título principal aplicando espaçamento vertical

    label_nome = tk.Label(janela, text="Nome do aluno:")
    label_nome.pack()                                  # Renderiza o texto indicador do Nome
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.pack(pady=5)                            # Renderiza a caixa de digitação para o Nome do aluno

    label_matricula = tk.Label(janela, text="Matrícula:")
    label_matricula.pack()                             # Renderiza o texto indicador da Matrícula
    entry_matricula = tk.Entry(janela, width=40)
    entry_matricula.pack(pady=5)                       # Renderiza a caixa de digitação para a Matrícula

    label_nota1 = tk.Label(janela, text="Nota 1:")
    label_nota1.pack()                                 # Renderiza o texto indicador da Nota 1
    entry_nota1 = tk.Entry(janela, width=20)
    entry_nota1.pack(pady=5)                           # Renderiza a caixa de digitação para a Nota 1

    label_nota2 = tk.Label(janela, text="Nota 2:")
    label_nota2.pack()                                 # Renderiza o texto indicador da Nota 2
    entry_nota2 = tk.Entry(janela, width=20)
    entry_nota2.pack(pady=5)                           # Renderiza a caixa de digitação para a Nota 2

    label_nota_final = tk.Label(janela, text="Nota Final:")
    label_nota_final.pack()                            # Renderiza o texto indicador da Nota Final
    entry_nota_final = tk.Entry(janela, width=20)
    entry_nota_final.pack(pady=5)                      # Renderiza a caixa de digitação para a Nota Final
    
    # -------------------------------
    # TABELA DE ALUNOS (TREEVIEW)
    # -------------------------------
    
    frame_tabela = tk.Frame(janela)                    # Cria o container isolado para agrupar tabela e scrollbar
    frame_tabela.pack(pady=20)                         # Renderiza o container na janela com espaçamento vertical

    tabela = ttk.Treeview(                             # Instancia a tabela estruturada com colunas específicas
        frame_tabela, 
        columns=("id", "nome", "matricula", "nota1", "nota2", "nota_final"), 
        show="headings", 
        height=8
    )

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)  # Instancia a barra de rolagem vinculada à tabela
    tabela.configure(yscrollcommand=scrollbar.set)    # Vincula o movimento da tabela de volta para a barra de rolagem

    tabela.pack(side="left")                           # Alinha e renderiza a tabela à esquerda dentro do container frame
    scrollbar.pack(side="right", fill="y")             # Alinha a barra à direita, preenchendo toda a altura disponível

    tabela.heading("id", text="ID")                    # Modifica o cabeçalho visível da coluna ID
    tabela.heading("nome", text="Nome")                # Modifica o cabeçalho visível da coluna Nome
    tabela.heading("matricula", text="Matrícula")      # Modifica o cabeçalho visível da coluna Matrícula
    tabela.heading("nota1", text="Nota 1")              # Modifica o cabeçalho visível da coluna Nota 1
    tabela.heading("nota2", text="Nota 2")              # Modifica o cabeçalho visível da coluna Nota 2
    tabela.heading("nota_final", text="Nota Final")     # Modifica o cabeçalho visível da coluna Nota Final

    tabela.column("id", width=50)                      # Ajusta a largura em pixels da coluna ID
    tabela.column("nome", width=200)                   # Ajusta a largura em pixels da coluna Nome
    tabela.column("matricula", width=100)              # Ajusta a largura em pixels da coluna Matrícula
    tabela.column("nota1", width=80)                   # Ajusta a largura em pixels da coluna Nota 1
    tabela.column("nota2", width=80)                   # Ajusta a largura em pixels da coluna Nota 2
    tabela.column("nota_final", width=100)             # Ajusta a largura em pixels da coluna Nota Final

    tabela.bind("<<TreeviewSelect>>", selecionar_aluno) # Associa o evento de clique na linha à função de preencher campos

    # -------------------------------
    # BOTÕES DE AÇÃO
    # -------------------------------

    botao_cadastrar = tk.Button(janela, text="Cadastrar", width=15, command=cadastrar_aluno)
    botao_cadastrar.pack(pady=5)                       # Instancia e renderiza o botão associado à inserção de dados

    botao_listar = tk.Button(janela, text="Listar", width=15, command=carregar_alunos)
    botao_listar.pack(pady=5)                          # Instancia e renderiza o botão associado à busca geral de dados

    botao_atualizar = tk.Button(janela, text="Atualizar", width=15, command=atualizar_dados)
    botao_atualizar.pack(pady=5)                       # Instancia e renderiza o botão associado à edição de dados

    botao_deletar = tk.Button(janela, text="Deletar", width=15, command=deletar_selected)
    botao_deletar.pack(pady=5)                         # Instancia e renderiza o botão associado à remoção de dados
        
    janela.mainloop()                                  # Dispara o loop contínuo do Tkinter mantendo a interface aberta
