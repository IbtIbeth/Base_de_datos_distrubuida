CREATE DATABASE sucursal;

-- TODO Create python connection user
CREATE USER 'python_interface'@'MASTER_HOST_DIRECTION' IDENTIFIED BY 'SECURE_PASSWORD';
GRANT ALL ON test.* TO 'python_interface'@'MASTER_HOST_DIRECTION';
-- Specific permissions
GRANT ALL ON mysql.* TO 'spider'@'MASTER_HOST_DIRECTION';


-- Create Server connections to the remote databases servers
CREATE OR REPLACE SERVER ServerMorelia FOREIGN DATA WRAPPER mysql
OPTIONS(HOST 'SLAVE1_HOST_DIRECTION', DATABASE 'sucursal', PORT 3306,
USER 'spider', PASSWORD 'spider');

CREATE OR REPLACE SERVER ServerPatzcuaro FOREIGN DATA WRAPPER mysql
OPTIONS(HOST 'SLAVE2_HOST_DIRECTION', DATABASE 'sucursal', PORT 3306,
USER 'spider', PASSWORD 'spider');

-- Create table for client
CREATE TABLE sucursal.CLIENTE (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    rfc VARCHAR(13) NOT NULL,
    sucursal VARCHAR(100) NOT NULL,
    PRIMARY KEY(id, sucursal)
)
ENGINE=Spider
COMMENT 'wrapper "mysql", table "CLIENTE"'
	PARTITION BY LIST COLUMNS (sucursal) (
	PARTITION p0 VALUES IN ("patzcuaro") COMMENT = 'srv "ServerPatzcuaro"',
	PARTITION p1 VALUES IN ("morelia") COMMENT = 'srv "ServerMorelia"'
);


-- Create table for address
CREATE TABLE sucursal.DIRECCION (
    id INT NOT NULL AUTO_INCREMENT,
    calle VARCHAR(100) NOT NULL,
    numero VARCHAR(5) NOT NULL,
    colonia VARCHAR(50) NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    cp INT(5) NOT NULL,
    sucursal VARCHAR(100) NOT NULL,
    PRIMARY KEY(id, sucursal)
)
ENGINE=Spider
COMMENT 'wrapper "mysql", table "DIRECCION"'
	PARTITION BY LIST COLUMNS (sucursal) (
	PARTITION p0 VALUES IN ("patzcuaro") COMMENT = 'srv "ServerPatzcuaro"',
	PARTITION p1 VALUES IN ("morelia") COMMENT = 'srv "ServerMorelia"'
);

CREATE TABLE sucursal.CLIENTE_DIRECCION(
	id_cliente INT NOT NULL,
	id_direccion INT NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    PRIMARY KEY (sucursal),
    KEY (id_cliente, id_direccion)
)
ENGINE=Spider
COMMENT 'wrapper "mysql", table "CLIENTE_DIRECCION"'
	PARTITION BY LIST COLUMNS (sucursal) (
	PARTITION p0 VALUES IN ("patzcuaro") COMMENT = 'srv "ServerPatzcuaro"',
	PARTITION p1 VALUES IN ("morelia") COMMENT = 'srv "ServerMorelia"'
);
