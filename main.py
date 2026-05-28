# Importa a função responsável por listar alunos
from database.crud import listar_alunos

# Executa a função e armazena os dados retornados
alunos = listar_alunos()

# Percorre cada aluno encontrado no banco
for aluno in alunos:

    # Exibe cada registro no terminal
    print(aluno)