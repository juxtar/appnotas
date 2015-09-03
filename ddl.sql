CREATE TABLE Notas(
id INTEGER PRIMARY KEY,
contenido TEXT NOT NULL,
fecha TEXT NOT NULL,
hora TEXT NOT NULL,
color TEXT NOT NULL
);

INSERT INTO notas
VALUES(null, 'Hola, esto es una prueba desde el Workbench', '2015-08-21', '23:26:00', 'ffffff');