import psycopg2.extras
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

class Game(BaseModel):
    name: str
    platform: str
    score: int
    review: str

#abre e retorna a conexão com o banco de dados
def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    return conn


@app.get("/")
def home():
    return {"message": "Bem-vindo ao GameNotes API!"}

#rota para listar todos os jogos
@app.get("/games")
def get_games():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    cursor.close()
    conn.close()
    return games

#rota para adicionar um jogo
@app.post("/games")
def add_game(game: Game):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (name, platform, score, review) VALUES (%s, %s, %s, %s)", (game.name, game.platform, game.score, game.review))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Jogo adicionado com sucesso!"}
    

#DELETE
@app.delete("/games/{id}")
def delete_game(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM games WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Jogo deletado com sucesso!"}