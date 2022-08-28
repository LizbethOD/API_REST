DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes(
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL);

INSERT INTO clientes(nombre,email) VALUES("Zayn","zayn@email.com");
INSERT INTO clientes(nombre,email) VALUES("Beti","beti@email.com");
INSERT INTO clientes(nombre,email) VALUES("Taylor","taylor@email.com");
INSERT INTO clientes(nombre,email) VALUES("Niall", "Niall@email.com");
INSERT INTO clientes(nombre,email) VALUES("User2","user2@email.com");
INSERT INTO clientes(nombre,email) VALUES("Liam","liam@email.com");
INSERT INTO clientes(nombre,email) VALUES("User","user@email.com");

.headers ON 
SELECT * FROM clientes;

DROP TABLE IF EXISTS usuarios; 

CREATE TABLE usuarios(
    username TEXT,
    password varchar(32),
    level INTEGER
);

CREATE UNIQUE INDEX index_usuario ON usuarios(username); 

INSERT INTO usuarios(username, password, level) VALUES('admin','21232f297a57a5a743894a0e4a801fc3',0);
INSERT INTO usuarios(username, password, level) VALUES('user','ee11cbb19052e40b07aac0ca060c23ee',1);

SELECT * FROM usuarios;