import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

def init_db():
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

class User(BaseModel):
    username: str
    password: str

@app.post('/register')
def register(user: User):
    try:
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (user.username, user.password))
            conn.commit()
            return {"message": "успішна реєстрація"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Користувач існує")


@app.post('/login')
def login(user: User):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (user.username,))
        row = c.fetchone()
        if not row or user.password != row[0]:
            raise HTTPException(status_code=400, detail="невірний логін або пароль")

    return {"message": "вхід успішний"}