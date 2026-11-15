CREATE TABLE vuelos (
vuelo_id VARCHAR(20) PRIMARY KEY,
origen VARCHAR(50) NOT NULL,
destino VARCHAR(50) NOT NULL,
fecha_salida TIMESTAMP NOT NULL,
disponibles INT NOT NULL CHECK (disponibles >= 0)
);

CREATE TABLE reservas (
reserva_id SERIAL PRIMARY KEY,
vuelo_id VARCHAR(20) NOT NULL REFERENCES vuelos(vuelo_id),
documento VARCHAR(20) NOT NULL,
estado VARCHAR(20) NOT NULL DEFAULT 'CONFIRMADA', 
reservada_en TIMESTAMP NOT NULL DEFAULT now()
);

INSERT INTO vuelos(vuelo_id, origen, destino, fecha_salida, disponibles)
VALUES ('VUELO-001', 'Tacna', 'Lima', '2026-11-20 08:30:00', 10);