import tkinter as tk                                    # Puxa o básico da biblioteca para criar janelas
from tkinter import messagebox, ttk                   # Traz os alertas e os componentes modernos como a tabela
from database.crud import (                            # Importa a nossa ponte de comunicação com o banco de dados
    inserir_aluno,
    listar_alunos,
    deletar_aluno,
    atualizar_aluno
)

def iniciar_sistema():                                 # Ponto de partida para abrir a interface do sistema

    janela = tk.Tk()                                   # Cria a janela principal que vai segurar o programa
    janela.title("Sistema de Registro de Notas")       # Dá um nome para a barra de título lá em cima
    janela.geometry("900x850")                         # Configura um tamanho confortável para caber tudo

    # -------------------------------------------------------------------------
    # TRAVAS DE SEGURANÇA PARA AS NOTAS
    # -------------------------------------------------------------------------
    def validar_notas(s1_str, s2_str, av_str, avs_str):
        try:
            if s1_str.strip() != "":                   # Só checa se o professor tiver digitado algo
                nota_s1 = float(s1_str)                # Tenta converter o texto em número com ponto decimal
                if nota_s1 < 0.0 or nota_s1 > 1.0:     # O Simulado 1 vale só de 0 a 1 ponto
                    messagebox.showerror("Erro de Limite", "Bloqueado: O Simulado 1 só aceita notas entre 0.0 e 1.0!")
                    return False                       # Cancela a operação e avisa o usuário do erro

            if s2_str.strip() != "":                   # Checa o segundo simulado apenas se não estiver em branco
                nota_s2 = float(s2_str)                # Faz a conversão para número
                if nota_s2 < 0.0 or nota_s2 > 1.0:     # O Simulado 2 também vale no máximo 1 ponto
                    messagebox.showerror("Erro de Limite", "Bloqueado: O Simulado 2 só aceita notas entre 0.0 e 1.0!")
                    return False                       # Trava o sistema caso passe do valor permitido

            if av_str.strip() != "":                   # Verifica a Prova Oficial (AV) se houver nota
                nota_av = float(av_str)                # Transforma o texto em número decimal
                if nota_av < 0.0 or nota_av > 10.0:    # A AV aceita notas de 0 a 10 redondo
                    messagebox.showerror("Erro de Limite", "Bloqueado: A AV só aceita notas entre 0.0 e 10.0!")
                    return False                       # Impede o avanço por segurança

            if avs_str.strip() != "":                  # Checa se o professor preencheu a prova de recuperação
                nota_avs = float(avs_str)              # Passa para float para poder comparar
                if nota_avs < 0.0 or nota_avs > 10.0:  # A prova substitutiva também teto máximo de 10
                    messagebox.showerror("Erro de Limite", "Bloqueado: A AVS só aceita notas entre 0.0 e 10.0!")
                    return False                       # Para tudo se a nota for absurda

            return True                                # Se passou por todos os testes sem travar, a nota é válida
            
        except ValueError:                             # Entra aqui se o usuário digitar letras ou usar vírgula
            messagebox.showerror("Erro de Digitação", "Insira apenas números válidos (use ponto para decimais, ex: 1.0)!")
            return False                               # Corta o processo por erro de digitação

    # -------------------------------------------------------------------------
    # AÇÕES DOS BOTÕES E LOGICA DO SISTEMA
    # -------------------------------------------------------------------------

    def cadastrar_aluno():
        nome = entry_nome.get()                        # Pega o que foi digitado no campo de Nome
        matricula = entry_matricula.get()              # Captura o texto do campo de Matrícula
        s1 = entry_simulado1.get()                     # Pega a string do Simulado 1
        s2 = entry_simulado2.get()                     # Pega a string do Simulado 2
        av = entry_av.get()                            # Pega a string da AV
        avs = entry_avs.get()                          # Captura a AVS se o professor já colocá-la agora
        nota_final = entry_nota_final.get()            # Lê a nota final se tiver sido digitada na mão

        if not validar_notas(s1, s2, av, avs):         # Roda as travas que criamos lá em cima
            return                                     # Se a validação der errado, sai da função na hora

        try:
            n_s1 = float(s1) if s1.strip() != "" else 0.0   # Se o campo estiver vazio, considera 0 para calcular
            n_s2 = float(s2) if s2.strip() != "" else 0.0   # Evita erros matemáticos tratando o vazio como zero
            n_av = float(av) if av.strip() != "" else 0.0   # Faz o mesmo tratamento para a prova AV
            
            nota_parcial = n_s1 + n_s2 + n_av          # Soma os três componentes para ver a situação atual
            
            if avs.strip() != "":                      # Se o professor já preencheu a nota da recuperação
                n_avs = float(avs)                     # Converte ela para fazer a matemática
                maior_nota_prova = max(n_av, n_avs)    # A AVS substitui a AV se for maior. Pegamos a melhor delas.
                nota_final_calculada = str(round(n_s1 + n_s2 + maior_nota_prova, 2)) # Nova média com a recuperação
            else:
                if nota_parcial >= 6.0:                # Se o aluno já somou 6 ou mais sem recuperação
                    nota_final_calculada = str(round(nota_parcial, 2)) # Ele está aprovado com essa nota
                else:
                    nota_final_calculada = ""          # Nota final fica vazia (o sistema vai gerar o "REC" na tabela)
        except ValueError:
            nota_final_calculada = ""                  # Proteção extra para não quebrar em casos imprevistos

        if nota_final.strip() != "":                   # Se o professor digitou uma nota final manualmente
            nota_final_calculada = nota_final          # A escolha do professor ignora o cálculo automático

        inserir_aluno(nome, matricula, s1, s2, av, avs, nota_final_calculada) # Manda os números limpos para o banco
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")  # Alerta o usuário que deu tudo certo
        carregar_alunos()                              # Atualiza a tabela na tela para mostrar o novo aluno

        entry_nome.delete(0, tk.END)                   # Limpa a caixa de Nome para o próximo cadastro
        entry_matricula.delete(0, tk.END)              # Limpa a caixa de Matrícula
        entry_simulado1.delete(0, tk.END)              # Reseta o campo do Simulado 1
        entry_simulado2.delete(0, tk.END)              # Reseta o campo do Simulado 2
        entry_av.delete(0, tk.END)                     # Limpa a caixa da AV
        entry_avs.delete(0, tk.END)                    # Limpa a caixa da AVS
        entry_nota_final.delete(0, tk.END)             # Limpa o campo da Nota Final

    def carregar_alunos():
        for item in tabela.get_children():             
            tabela.delete(item)                        # Limpa as linhas da tabela da tela para não duplicar dados

        alunos = listar_alunos()                       # Faz o SELECT no banco e traz a lista atualizada
        
        for aluno in alunos:                           
            dados_limpos = ["" if valor is None else str(valor) for valor in aluno] # Troca os 'None' do banco por texto vazio
            
            try:
                n_s1 = float(dados_limpos[3]) if dados_limpos[3] != "" else 0.0  # Captura a nota do Simulado 1 da lista
                n_s2 = float(dados_limpos[4]) if dados_limpos[4] != "" else 0.0  # Captura a nota do Simulado 2
                n_av = float(dados_limpos[5]) if dados_limpos[5] != "" else 0.0  # Captura a nota da AV
                nota_parcial = n_s1 + n_s2 + n_av      # Soma tudo para analisar o status do aluno
            except ValueError:
                nota_parcial = 0.0                     # Se der erro, assume 0 temporariamente

            if nota_parcial < 6.0 and dados_limpos[6] == "": # Se a soma deu menos que 6 e não tem nota na AVS
                dados_limpos[6] = "REC"                # Coloca "REC" na coluna de AVS apenas para exibição visual
                tabela.insert("", tk.END, values=dados_limpos, tags=("recuperacao",)) # Insere com a tag de cor
            else:
                tabela.insert("", tk.END, values=dados_limpos) # Passou ou já tem nota, insere na tabela normalmente

        tabela.tag_configure("recuperacao", foreground="red", font=("Arial", 10, "bold")) # Pinta as linhas 'REC' de vermelho

    def atualizar_dados():
        nome = entry_nome.get()                        # Pega o nome modificado
        matricula = entry_matricula.get()              # Pega a matrícula do aluno selecionado
        s1 = entry_simulado1.get()                     # Pega o novo valor do Simulado 1
        s2 = entry_simulado2.get()                     # Pega o novo valor do Simulado 2
        av = entry_av.get()                            # Pega o novo valor da AV
        avs = entry_avs.get()                          # Pega a nota da AVS preenchida pelo professor
        nota_final = entry_nota_final.get()            # Lê o campo da nota final

        if not validar_notas(s1, s2, av, avs):         # Passa as novas notas pelo pente fino de segurança
            return                                     # Se estiverem fora do limite, cancela a alteração

        try:
            n_s1 = float(s1) if s1.strip() != "" else 0.0   # Trata campo em branco como 0
            n_s2 = float(s2) if s2.strip() != "" else 0.0   # Trata campo em branco como 0
            n_av = float(av) if av.strip() != "" else 0.0   # Trata campo em branco como 0
            
            nota_parcial = n_s1 + n_s2 + n_av          # Refaz a somatória das notas normais
            
            if avs.strip() != "":                      # Se o professor acabou de aplicar a prova de recuperação
                n_avs = float(avs)                     # Converte a nota para número
                nota_final_calculada = str(round(n_s1 + n_s2 + max(n_av, n_avs), 2)) # Recalcula usando a melhor prova
            else:
                if nota_parcial >= 6.0:                # Se as notas originais já batem a média
                    nota_final_calculada = str(round(nota_parcial, 2)) # Garante a aprovação direta
                else:
                    nota_final_calculada = ""          # Sem AVS e abaixo de 6, limpa a nota final para ficar em REC
        except ValueError:
            nota_final_calculada = ""                  # Evita travamento em casos excepcionais

        if nota_final.strip() != "":                   # Se o professor preencheu a nota final por fora
            nota_final_calculada = nota_final          # Usa a nota manual informada

        atualizar_aluno(nome, matricula, s1, s2, av, avs, nota_final_calculada) # Executa o UPDATE seguro no banco de dados
        carregar_alunos()                              # Recarrega a tabela visual imediatamente
        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!") # Mostra pop-up de sucesso
    
        entry_nome.delete(0, tk.END)                   # Deixa os campos vazios e limpos para o uso seguinte
        entry_matricula.delete(0, tk.END)              
        entry_simulado1.delete(0, tk.END)              
        entry_simulado2.delete(0, tk.END)              
        entry_av.delete(0, tk.END)                     
        entry_avs.delete(0, tk.END)                    
        entry_nota_final.delete(0, tk.END)             

    def deletar_selected():
        item_selecionado = tabela.selection()          # Vê qual linha o usuário clicou na tabela
        
        if not item_selecionado:                       # Se ele clicou no botão sem selecionar ninguém
            messagebox.showwarning("Aviso", "Selecione um aluno para deletar.") # Exibe um aviso educativo
            return                                     # Aborta a exclusão

        dados_aluno = tabela.item(item_selecionado[0]) # Coleta o dicionário de dados daquela linha
        valores = dados_aluno["values"]                # Extrai a lista de valores das colunas
        matricula = str(valores[2]).strip()            # A matrícula está na coluna 2, ela é a chave de busca

        deletar_aluno(matricula)                       # Aciona o comando DELETE no PostgreSQL passando a matrícula
        carregar_alunos()                              # Apaga a linha da tabela na tela
        messagebox.showinfo("Sucesso", "Aluno removido com sucesso!") # Mostra a mensagem de confirmação

        entry_nome.delete(0, tk.END)                   # Reseta todos os campos superiores por organização
        entry_matricula.delete(0, tk.END)              
        entry_simulado1.delete(0, tk.END)              
        entry_simulado2.delete(0, tk.END)              
        entry_av.delete(0, tk.END)                     
        entry_avs.delete(0, tk.END)                    
        entry_nota_final.delete(0, tk.END)             

    def selecionar_aluno(event):
        item_selecionado = tabela.selection()          # Identifica qual linha acabou de ser clicada

        if not item_selecionado:                       
            return                                     # Se for um clique perdido, ignora

        dados_aluno = tabela.item(item_selecionado[0]) # Captura as informações da linha
        valores = dados_aluno["values"]                # Separa os valores coluna por coluna

        entry_nome.delete(0, tk.END)                   # Limpa os campos antigos antes de carregar o aluno novo
        entry_matricula.delete(0, tk.END)              
        entry_simulado1.delete(0, tk.END)              
        entry_simulado2.delete(0, tk.END)              
        entry_av.delete(0, tk.END)                     
        entry_avs.delete(0, tk.END)                    
        entry_nota_final.delete(0, tk.END)             

        entry_nome.insert(0, valores[1])               # Joga o nome da tabela na caixa de texto
        entry_matricula.insert(0, valores[2])          # Preenche a matrícula lá em cima
        entry_simulado1.insert(0, valores[3])          # Preenche a nota do Simulado 1
        entry_simulado2.insert(0, valores[4])          # Preenche a nota do Simulado 2
        entry_av.insert(0, valores[5])                 # Preenche a nota da AV
        
        val_avs = "" if str(valores[6]) == "REC" else valores[6] # Se na tela estiver "REC", limpa para o professor dar a nota
        entry_avs.insert(0, val_avs)                   # Insere o valor real da AVS na caixa de digitação
        entry_nota_final.insert(0, valores[7])         # Preenche a nota final na caixa correspondente

    # -------------------------------------------------------------------------
    # CONSTRUÇÃO DA INTERFACE GRÁFICA (CAMPOS E TEXTOS)
    # -------------------------------------------------------------------------

    titulo = tk.Label(janela, text="Sistema de Registro de Notas", font=("Arial", 18, "bold"))
    titulo.pack(pady=20)                               # Desenha o título principal centralizado no topo da janela

    label_nome = tk.Label(janela, text="Nome do aluno:")
    label_nome.pack()                                  # Rótulo para indicar onde colocar o nome do aluno
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.pack(pady=3)                            # Campo de texto para digitação do nome completo

    label_matricula = tk.Label(janela, text="Matrícula:")
    label_matricula.pack()                             # Rótulo para indicar o campo de identificação único
    entry_matricula = tk.Entry(janela, width=40)
    entry_matricula.pack(pady=3)                       # Caixa para digitar a matrícula do estudante

    label_simulado1 = tk.Label(janela, text="Simulado 1 (Max 1.0):") #(Max 1.0)  a nota maxima.
    label_simulado1.pack()                             # Texto indicativo do teto da primeira nota curta
    entry_simulado1 = tk.Entry(janela, width=20)
    entry_simulado1.pack(pady=3)                       # Caixa de entrada para a nota do primeiro simulado

    label_simulado2 = tk.Label(janela, text="Simulado 2 (Max 1.0):") #(Max 1.0) nota maxima.
    label_simulado2.pack()                             # Texto explicativo para o segundo simulado do bimestre
    entry_simulado2 = tk.Entry(janela, width=20)
    entry_simulado2.pack(pady=3)                       # Caixa de entrada para a nota do segundo simulado

    label_av = tk.Label(janela, text="AV:")            #(Max 10.0)
    label_av.pack()                                    # Rótulo da avaliação oficial principal
    entry_av = tk.Entry(janela, width=20)
    entry_av.pack(pady=3)                              # Caixa para receber a nota da prova AV

    label_avs = tk.Label(janela, text="AVS:")           #se o aluno ficar de avs, aparecera REC. tendo por media abaixo de 6.
    label_avs.pack()                                    # Indica o campo da prova de recuperação/substitutiva
    entry_avs = tk.Entry(janela, width=20, state="normal") # Campo mantido desbloqueado para o professor digitar a nota real
    entry_avs.pack(pady=3)                             

    label_nota_final = tk.Label(janela, text="Nota Final:")
    label_nota_final.pack()                            # Rótulo informativo sobre o automatismo da média
    entry_nota_final = tk.Entry(janela, width=20, state="normal") # Campo aberto que aceita tanto automação quanto ajuste manual
    entry_nota_final.pack(pady=3)                      
    
    # -------------------------------------------------------------------------
    # DESIGN E LINHAS DA TABELA (ESTILIZAÇÃO)
    # -------------------------------------------------------------------------
    
    estilo = ttk.Style()
    estilo.theme_use("clam")                           # Aplica um tema que aceita customização de bordas celulares
    
    estilo.configure(
        "Treeview", 
        rowheight=25,                                  # Configura uma altura confortável para a leitura das linhas
        background="white",                            # Fundo das linhas da tabela fica inteiramente branco
        fieldbackground="white",                       # Fundo da área vazia da tabela acompanha a cor branca
        foreground="black"                             # Letras das notas e nomes em preto fosco padrão
    )
    
    estilo.configure("Treeview", bordercolor="#CCCCCC", borderwidth=1) # Cria as bordas finas em cinza claro ao redor das células
    estilo.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Força o layout a renderizar a grade horizontal e vertical

    frame_tabela = tk.Frame(janela)                    # Cria uma caixinha invisível para organizar a tabela e a barra
    frame_tabela.pack(pady=20)                         # Dá um espaçamento externo para respirar o visual

    tabela = ttk.Treeview(                             
        frame_tabela, 
        columns=("id", "nome", "matricula", "simulado1", "simulado2", "av", "avs", "nota_final"), # Define a ordem das colunas
        show="headings",                               # Esconde a coluna fantasma que o Tkinter gera por padrão
        height=8                                       # Define que a tabela mostrará 8 alunos por vez na tela
    )

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview) # Cria uma barra de rolagem clássica em pé
    tabela.configure(yscrollcommand=scrollbar.set)    # Linka o movimento da barra com o movimento vertical da tabela

    tabela.pack(side="left")                           # Encosta a tabela no lado esquerdo do frame
    scrollbar.pack(side="right", fill="y")             # Encosta a barra de rolagem na direita preenchendo toda a altura

    tabela.heading("id", text="ID")                    # Texto do cabeçalho da coluna ID
    tabela.heading("nome", text="Aluno")               # Texto do cabeçalho da coluna do Nome
    tabela.heading("matricula", text="Matrícula")      # Texto do cabeçalho da Matrícula
    tabela.heading("simulado1", text="Simulado 1")    # Texto do cabeçalho do Simulado 1
    tabela.heading("simulado2", text="Simulado 2")    # Texto do cabeçalho do Simulado 2
    tabela.heading("av", text="AV")                    # Texto do cabeçalho da AV
    tabela.heading("avs", text="AVS")                  # Texto do cabeçalho da AVS
    tabela.heading("nota_final", text="Nota Final")    # Texto do cabeçalho da Nota Final

    tabela.column("id", width=40, anchor="center")     # Centraliza o ID e define largura de 40 pixels
    tabela.column("nome", width=180, anchor="center")  # Centraliza o Nome com espaço de 180 pixels
    tabela.column("matricula", width=100, anchor="center") # Centraliza a Matrícula na célula
    tabela.column("simulado1", width=95, anchor="center") # Centraliza as notas do primeiro simulado
    tabela.column("simulado2", width=95, anchor="center") # Centraliza as notas do segundo simulado
    tabela.column("av", width=65, anchor="center")     # Alinha a nota da prova AV perfeitamente no meio
    tabela.column("avs", width=65, anchor="center")    # Alinha a nota da AVS/REC de forma centralizada
    tabela.column("nota_final", width=160, anchor="center") # Centraliza a exibição da nota final calculada

    tabela.bind("<<TreeviewSelect>>", selecionar_aluno) # Monitora cliques na tabela para carregar as caixas de texto

    # -------------------------------------------------------------------------
    # BOTÕES INFERIORES DE GERENCIAMENTO
    # -------------------------------------------------------------------------
    botao_cadastrar = tk.Button(janela, text="Cadastrar", width=15, command=cadastrar_aluno)
    botao_cadastrar.pack(pady=3)                       # Botão que ativa a função de inserção de dados

    botao_listar = tk.Button(janela, text="Listar", width=15, command=carregar_alunos)
    botao_listar.pack(pady=3)                          # Botão que recarrega os dados lidos do banco

    botao_atualizar = tk.Button(janela, text="Atualizar", width=15, command=atualizar_dados)
    botao_atualizar.pack(pady=3)                       # Botão que grava as modificações efetuadas nas notas

    botao_deletar = tk.Button(janela, text="Deletar", width=15, command=deletar_selected)
    botao_deletar.pack(pady=3)                         # Botão que dispara a exclusão permanente do registro
        
    carregar_alunos()                                  # Executa uma listagem automática assim que o programa se abre
    janela.mainloop()                                  # Trava o script mantendo a janela aberta e escutando cliques