SELECT * FROM vuelos;

UPDATE vuelos SET disponibles = -1 WHERE vuelo_id = 'VUELO-001';

INSERT INTO reservas (vuelo_id, documento)
VALUES ('VUELO-999', '12345678');

INSERT INTO reservas (documento)
VALUES('12345678')

INSERT INTO reservas (vuelo_id, documento)
VALUES ('VUELO-001', '12345678')

SELECT * FROM reservas;