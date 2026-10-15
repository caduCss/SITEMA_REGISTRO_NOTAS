# Sistema de Registro de Notas de Alunos 

Um sistema de gerenciamento escolar desktop completo, desenvolvido em **Python**, utilizando a biblioteca gráfica **Tkinter** para a interface de usuário e o banco de dados relacional **SQLite3** para a persistência real e segura dos dados.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python                             # Linguagem base do projeto
* **Interface Gráfica:** Tkinter                    # Responsável pelas janelas, botões e tabelas
* **Banco de Dados:** SQLite3                       # Banco de dados relacional robusto
* **Driver de Conexão:** SQLite3                    # Ponte de comunicação sendo feita pelo SQLite3

---

## 📂 Estrutura do Projeto

O projeto foi construído seguindo princípios de arquitetura modular, separando as responsabilidades de interface, lógica de banco de dados e scripts de configuração:

```text
Sistema_Registro_Notas/
│
├── database/                     # Módulo responsável pelo banco de dados
│   ├── conexao.py                # Cria a conexão e a tabela de alunos
│   ├── crud.py                   # Cadastra, lista, atualiza e exclui alunos
│   └── sistema_notas.db           # Banco SQLite que armazena os registros
│
├── interface/                    # Módulo da interface gráfica
│   ├── __init__.py               # Identifica a pasta como um pacote Python
│   └── tela_principal.py          # Janela, campos, botões e tabela de alunos
│
├── SQL/                          # Pasta para scripts SQL
│   └── script_banco.sql          # Script SQL de referência do projeto
│
├── main.py                       # Ponto de entrada: inicia o sistema
│
└── README.md                     # Documentação do projeto

## 📂 Atualizações do Projetos

* Foi trocado o PostgreSQL pelo Sqlite3