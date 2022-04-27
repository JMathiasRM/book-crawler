import psycopg2
import psycopg2.extras
import os

class Database():
    def __init__(self):
        # if necessary, replace with working credentials
        self.conn = psycopg2.connect(
            database = os.getenv("POSTGRES_DB"),
            host = os.getenv("POSTGRES_HOST"),
            port = os.getenv("POSTGRES_PORT"),
            user = os.getenv("POSTGRES_USER_DEV"),
            password = os.getenv("POSTGRES_PASSWORD_DEV")
        )
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS joao_mathias_livros(
                id SERIAL UNIQUE PRIMARY KEY,
                titulo VARCHAR(255),
                categoria VARCHAR(63),
                preco FLOAT,
                estoque INT,
                descricao VARCHAR(4095),
                data VARCHAR(15))
            '''
        )
        self.conn.commit()
    
    def __del__(self):
        self.cur.close()
        self.conn.close()
    
    def fetchN(self, cat: str, n: int):
        self.cur.execute(
            f'''
            SELECT titulo, categoria, preco, estoque, descricao, data
            FROM joao_mathias_livros
            WHERE categoria LIKE '{cat}'
            '''
        )
        self.conn.commit()
        return self.cur.fetchmany(n)
    
    def fetchStockN(self, cat: str, n: int):
        self.cur.execute(
            f'''
            SELECT titulo, categoria, preco, estoque, descricao, data
            FROM joao_mathias_livros
            WHERE categoria LIKE '{cat}' AND estoque < {n}
            '''
        )
        self.conn.commit()
        return self.cur.fetchall()
    
    def insert(self, books):
        for b in books:
            self.cur.execute(
                f'''
                INSERT INTO joao_mathias_livros (titulo, categoria, preco, estoque, descricao, data)
                VALUES ('{b['Título']}','{b['Categoria']}',{b['Preço']},{b['Estoque']},'{b['Descrição']}','{b['Data de crawleamento']}')
                '''
            )
            self.conn.commit()

    def deleteCat(self, cat: str):
        self.cur.execute(
            f'''
            DELETE
            FROM joao_mathias_livros
            WHERE categoria like '{cat}'
            '''
        )
        self.conn.commit()