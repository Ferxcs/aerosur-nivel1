import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
CONEXION = os.getenv("DATABASE_URL")

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "API de AeroSur funcionando"}

#RUTA NUEVA
@app.get("/vuelos")
def listar_vuelos():
    with psycopg.connect(CONEXION, row_factory=dict_row) as conexion:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM vuelos")
            return cursor.fetchall()

