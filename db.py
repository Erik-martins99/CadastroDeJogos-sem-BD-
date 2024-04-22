import pyodbc

# Configurar os detalhes da conexão
dados_conexao = (
    "Driver={SQL Server};"
    "Server=HCDAPC001\DETRANBA;"
    "Database=ambiente_teste;"
    "Trusted_Connection=yes;"  # Use Trusted_Connection=yes para autenticação do Windows
)

# Estabelecer a conexão com o banco de dados
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

# Definir a instrução SQL para criar a tabela
sql_create_table = """
CREATE TABLE teste (
    ID INT PRIMARY KEY,
    Nome VARCHAR(255),
    Idade INT
);
"""

# Executar a instrução SQL para criar a tabela
cursor.execute(sql_create_table)

# Confirmar a transação para efetivar a criação da tabela
conexao.commit()

# Fechar a conexão
conexao.close()

print("Tabela criada com sucesso!")