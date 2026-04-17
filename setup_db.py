import psycopg2
import os

url_banco = os.getenv("DATABASE_URL")

conn = psycopg2.connect(url_banco, sslmode="require")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS games;")

cursor.execute("""
    CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    score INT CHECK (score >= 1 AND score <= 10),
    review TEXT
);""")

conn.commit()
cursor.close()
conn.close()

print("Tabela games criada com sucesso!")

