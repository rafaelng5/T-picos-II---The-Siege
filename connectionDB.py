import mysql.connector
from mysql.connector import Error

# Função para criar a conexão com o banco de dados
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Função para executar uma consulta
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Função para ler os resultados de uma consulta
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Função para inserir um novo jogador
def insert_jogador(connection, jogador_nome):
    insert_jogador_query = f"""
    INSERT INTO jogador (nome) VALUES ('{jogador_nome}');
    """
    execute_query(connection, insert_jogador_query)

# Função para inserir uma nova fase
def insert_fase(connection, fase_nome):
    insert_fase_query = f"""
    INSERT INTO fase (nome) VALUES ('{fase_nome}');
    """
    execute_query(connection, insert_fase_query)

# Função para inserir uma nova pontuação
def insert_pontuacao(connection, jogador_nome, fase_nome, pontuacao_valor, tempo_valor):
    insert_pontuacao_query = f"""
    INSERT INTO pontuacao (id_jogador, id_fase, pontuacao, tempo) 
    VALUES (
        (SELECT id FROM jogador WHERE nome = '{jogador_nome}'), 
        (SELECT id FROM fase WHERE nome = '{fase_nome}'), 
        {pontuacao_valor}, '{tempo_valor}'
    );
    """
    execute_query(connection, insert_pontuacao_query)

# Função para exibir todas as pontuações
def select_all_pontuacoes(connection):
    select_pontuacao_query = """
    SELECT 
        jogador.nome AS jogador,
        fase.nome AS fase,
        pontuacao.pontuacao,
        pontuacao.tempo
    FROM 
        pontuacao
    INNER JOIN 
        jogador ON pontuacao.id_jogador = jogador.id
    INNER JOIN 
        fase ON pontuacao.id_fase = fase.id;
    """
    pontuacoes = read_query(connection, select_pontuacao_query)

    for pontuacao in pontuacoes:
        print(pontuacao)

# Variáveis de conexão ao banco de dados
host_name = "127.0.0.1"
user_name = "root"
user_password = "root"
db_name = "TheSiege"

# Conectar ao banco de dados 
connection = create_connection(host_name, user_name, user_password, db_name)

# Inserir um novo jogador 

# Exemplo Inserir uma nova fase 
insert_fase(connection, "Fase 4")

# Exemplo Inserir uma nova pontuação 
insert_pontuacao(connection, "Ana", "Fase 4", 3000, "00:02:50")

# Ler e exibir todas as pontuações
select_all_pontuacoes(connection)