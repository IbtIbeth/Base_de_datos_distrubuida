-- Create a new database
CREATE DATABASE sucursal;

-- Select sucursal databse
USE sucursal;

-- Create table for client
CREATE TABLE CLIENTE (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    rfc VARCHAR(13) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    PRIMARY KEY(id));

-- Create table for direction
CREATE TABLE DIRECCION (
    id INT NOT NULL AUTO_INCREMENT,
    calle VARCHAR(100) NOT NULL,
    numero VARCHAR(5) NOT NULL,
    colonia VARCHAR(50) NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    cp INT(5) NOT NULL,
    sucursal VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
    -- FOREIGN KEY (id_cliente) REFERENCES sucursal.CLIENTE(id) ON DELETE CASCADE
);

-- Create transitive table for client and address
CREATE TABLE CLIENTE_DIRECCION(
	id_cliente INT NOT NULL,
	id_direccion INT NOT NULL,
  sucursal VARCHAR(100) NOT NULL,
	FOREIGN KEY (id_cliente) REFERENCES sucursal.CLIENTE(id) ON DELETE CASCADE,
	FOREIGN KEY (id_direccion) REFERENCES sucursal.DIRECCION(id) ON DELETE CASCADE
);


-- Create user for master connection
-- using the IP address from the remote server
CREATE USER 'spider'@'MASTER_HOST_DIRECTION' IDENTIFIED BY 'spider';
GRANT ALL ON sucursal.* TO 'spider'@'MASTER_HOST_DIRECTION';
GRANT ALL ON mysql.* TO 'spider'@'MASTER_HOST_DIRECTION';
