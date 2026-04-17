import os
import psycopg2 
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
def get_conexao():
    try:
        conexao = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        print("CONEXÃO ESTABELECIDA!")
        return conexao

    except Exception as e:
        print(f"ERRO DE CONEXÃO: {e}")
        return None

def cria_tabela(conexao):
    try:
        with conexao.cursor() as cursor:

            #Criar Tabela
            comando_sql_create = """ 
                CREATE TABLE IF NOT EXISTS Consultas (
                    id SERIAL PRIMARY KEY,
                    ip VARCHAR(50) NOT NULL,
                    valor_total DECIMAL(10, 2),
                    cupom DECIMAL(10,2),
                    cashback DECIMAL(10, 2),
                    vip BOOLEAN,
                    data_consulta TIMESTAMPTZ DEFAULT NOW()
            ); 
            """
            cursor.execute(comando_sql_create)
            conexao.commit()
            print("TABELA INICIADA!")
        return conexao
    
    except Exception as e:
        print(f"ERRO NA CRIAÇÃO DA TABELA: {e}")
        return None
    
def preenche_tabela(conexao, ip, valor_total, cupom, cashback, vip):   
    try:
        with conexao.cursor() as cursor:
            #Preencher Tabela
            comando_sql_insert = """
                        INSERT INTO Consultas(ip, valor_total, cupom, cashback, vip)
                        VALUES (%(meu_ip)s, %(meu_valor)s,%(cupom_usado)s,%(meu_cashback)s,%(is_vip)s);
                                """
            dados_consulta = {
                "meu_ip":ip,
                "meu_valor":valor_total,
                "cupom_usado":cupom,
                "meu_cashback":cashback,
                "is_vip":vip        
            }
            cursor.execute(comando_sql_insert, dados_consulta)
            conexao.commit()
            print("DADOS SALVOS COM SUCESSO NO HISTÓRICO!")
            

    except Exception as e:
        print(f"ERRO DE BANCO: {e}")

def consulta_tabela_ip(conexao, ip):
    try:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            comando_sql_consulta = """ 
                SELECT
                    id,
                    valor_total,
                    cupom,
                    cashback,
                    vip,
                    TO_CHAR(data_consulta, 'DD/MM/YYYY às HH24:MI') as data_formatada
                FROM Consultas
                WHERE ip = %(meu_ip)s
                ORDER BY id DESC;
            """
            cursor.execute(comando_sql_consulta,{"meu_ip": ip})
            return cursor.fetchall()
        
    except Exception as e:
        print(f"ERRO NA CONSULTA: {e}")