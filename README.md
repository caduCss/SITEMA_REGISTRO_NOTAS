# Sistema de Registro de Notas de Alunos 

Um sistema de gerenciamento escolar desktop completo, desenvolvido em **Python**, utilizando a biblioteca gráfica **Tkinter** para a interface de usuário e o banco de dados relacional **PostgreSQL** para a persistência real e segura dos dados.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python                             # Linguagem base do projeto
* **Interface Gráfica:** Tkinter                     # Responsável pelas janelas, botões e tabelas
* **Banco de Dados:** PostgreSQL                    # Banco de dados relacional robusto
* **Driver de Conexão:** psycopg2-binary            # Ponte de comunicação entre Python e PostgreSQL

---

## 📂 Estrutura do Projeto

O projeto foi construído seguindo princípios de arquitetura modular, separando as responsabilidades de interface, lógica de banco de dados e scripts de configuração:

```text
SISTEMA_NOTAS/
│
├── main.py                  # Ponto de entrada (inicializa o sistema)
├── README.md                # Documentação do projeto
├── requerements.txt         # Listagem de dependências do projeto
│
├── database/                # Módulo de persistência de dados
│   ├── __init__.py          # Inicializador do pacote python
│   ├── conexao.py           # Configuração e abertura de conexão com o PostgreSQL
│   └── crud.py              # Funções SQL organizadas (Insert, Select, Update,Delete)
│
├── interface/               # Módulo da interface visual (GUI)
│   ├── __init__.py          # Inicializador do pacote python
│   └── tela_principal.py    # Construção da janela Tkinter, inputs e eventos
│
└── SQL/                     # Documentação de apoio ao banco
    └── script_banco.sql     # Script físico de criação da tabela de alunos


# OBS: não foi substituido o postgresql por sqlite.