import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

#para el checkpoint 5, los datos no pueden ir fijos en el codigo. Los datos lo manda el cliente en la petición, para recibirlos usamos Pydantic
from pydantic import BaseModel
#para la funcion reservar_vuelos \/ abajo
class NuevaReserva(BaseModel):
    vuelo_id: str
    documento: str

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



#RUTA NUEVA LA DE RESERVAS
@app.post("/reservas")
def reservar_vuelos(datos: NuevaReserva):
    with psycopg.connect(CONEXION, row_factory=dict_row) as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO reservas (vuelo_id, documento) VALUES (%s, %s) RETURNING *",
                (datos.vuelo_id, datos.documento),
            )
            return cursor.fetchone()