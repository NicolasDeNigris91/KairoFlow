import psycopg2
from psycopg2 import sql

print("Tentando criar banco de dados 'kairoflow'...")

try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres123",
        port=5432
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Conectado ao PostgreSQL")
    
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'kairoflow';")
    exists = cursor.fetchone()
    
    if exists:
        print("Banco 'kairoflow' já existe")
    else:
        cursor.execute("CREATE DATABASE kairoflow;")
        print("Banco 'kairoflow' criado com sucesso!")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f" Erro de conexão: {e}")
    
except Exception as e:
    print(f" Erro: {e}")