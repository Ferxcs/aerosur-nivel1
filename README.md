# AeroSur – Nivel 1 (reconstrucción)

API de reservas de vuelos con FastAPI y PostgreSQL, reconstruida desde cero
para afianzar lo aprendido. Cada checkpoint documenta qué hice, cómo lo hice
y qué aprendí.

## Tecnologías

- PostgreSQL 16 en Docker
- Python + FastAPI (desde el checkpoint 2)
- Git y GitHub

## Cómo levantar la base de datos

Requisito: el contenedor `postgres-dev` corriendo.

```bash
docker start postgres-dev
docker exec postgres-dev psql -U postgres -c "CREATE DATABASE aerosur_n1;"
docker exec -i postgres-dev psql -U postgres -d aerosur_n1 < db/schema.sql
```

## Checkpoints

- [X] 1. Base de datos
- [X] 2. Entorno Python
- [X] 3. API mínima
- [X] 4. Leer vuelos
- [X] 5. Crear reserva (transacción)
- [ ] 6. Consultar reserva

## Checkpoint 1: Base de datos

### Qué hice

Definí en `db/schema.sql` dos tablas, `vuelos` y `reservas`, y un vuelo de prueba.

### Reglas de integridad

| Regla | Dónde | Qué impide |
|---|---|---|
| `PRIMARY KEY` | `vuelos.vuelo_id`, `reservas.reserva_id` | Identificadores repetidos |
| `CHECK (disponibles >= 0)` | `vuelos` | Asientos en negativo |
| `REFERENCES vuelos` | `reservas.vuelo_id` | Reservas de vuelos que no existen |
| `NOT NULL` | `reservas.vuelo_id` | Reservas sin vuelo |

### Pruebas realizadas

| Prueba | Resultado |
|---|---|
| Dejar `disponibles` en -1 | Rechazado (`vuelos_disponibles_check`) |
| Reserva para `VUELO-999` | Rechazado (`reservas_vuelo_id_fkey`) |
| Reserva sin `vuelo_id` | Rechazado (restricción `NOT NULL`) |
| Reserva válida para `VUELO-001` | Aceptada; `estado` y fecha se llenan solos |

### Qué aprendí

- `REFERENCES` no impide valores vacíos: hace falta `NOT NULL` para cerrar ese hueco.
- `SERIAL` usa un contador que no retrocede, aunque el `INSERT` falle.
  Por eso los ids pueden tener huecos: mi primera reserva fue la número 5.
- `TIMESTAMP` sin zona horaria guarda la hora del servidor (UTC en el contenedor).
  `TIMESTAMPTZ` guarda el instante exacto.
- El esquema va en un archivo versionado; las pruebas van en el borrador de SQLTools.

## Decisiones de diseño

- **Cada fila de `vuelos` es una salida concreta.** En un sistema real habría dos
  tablas: `vuelos` (la ruta) y `salidas` (fecha y asientos de cada día). Es una
  simplificación intencional para este nivel.
- **Llave natural:** el código del vuelo es la llave primaria.


## Checkpoint 2: Entorno Python
## Cómo preparar el entorno Python

```bash
python -m venv venv
source venv/Scripts/activate      # Git Bash
# .\venv\Scripts\Activate.ps1     # PowerShell
pip install -r requirements.txt
```

### Qué aprendí

- El venv no va al repo; requirements.txt es su receta, igual que schema.sql lo es de la base.
- pip freeze lista también las dependencias de mis dependencias.
- En Git Bash se activa con source venv/Scripts/activate; el .ps1 es para PowerShell.
- En bash, los corchetes van entre comillas.


## Checkpoint 3: Api Mínima
### Chuleta
- Desde fastapi importamos FastApi.
- Creamos una variable app, donde guardaremos nuestra API
- Definimos la ruta, decoramos, creamos la funcion y esto lo guardamos en app.
- Por ultimo arrancamos con uvicorn

## Checkpoint 4: Leer vuelos

### Qué Hice

Bueno en esta checkpoint “creé una función y la decoré con @app.get para asignarle la ruta /vuelos, esta función nos permite hacer un SELECT y por eso podemos ver nuestra tabla vuelos

### Qué aprendí

Guardamos los datos sensibles en el archivo .env para poder leerlos y cargarlos como variables de entorno.

Por qué lo hicimos así? pues justamente para el momento de hacer push estas credenciales o datos sensibles no esten en el github
- pero cometi un error, se subió mi .vscode y ahi esta todo :p xd

en fin con with(cierra la conexión sola aunque algo falle)

## Checkpoint 5: Crear reserva (transacción)

- POST/reservas descuenta el asiento y crea la reserva en una transacción.
- Responde 409 si no hay asientos