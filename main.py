from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy import text
import sqlalchemy
from dotenv import dotenv_values
import sys
from sqlalchemy.engine.base import Connection
import actions as act
import unidecode
import json


config = dotenv_values(".env") # take environment variables from .env.


def print_menu():
    """
    Print menu
    """
    print("-"*60)
    print("   | BIENVENIDE |   ".center(60, "-"))
    print("-"*60)
    print("Opciones disponibles:")
    print("[0] - Listar clientes")
    print("[1] - Buscar usuario por RFC, nombre o domicilio")
    print("[2] - Crear usuario")
    print("[3] - Actualizar usuario")
    print("[4] - Listar direcciones")
    print("[5] - Crear dirección")
    print("[6] - Actualizar dirección")
    print("[7] - Crear tabla")
    print("[X] - Salir")


def load_main_connection():
    """
    Function to load the main connection.
    """
    database = config.get("DATABASE")
    user = config.get("USER_DB")
    password = config.get("PASSWORD")
    host = config.get("HOST")
    port = config.get("PORT")
    connection = create_connection(user, password, host, port, database)

    return connection.connect()


def create_connection(user, password, host, port, database):
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    return engine.connect()


def create_new_table(**kwargs):
    i = 0
    query = ""
    for value in kwargs.items():
        if i == 0: #asumo el primer valor del input es el nombre de la tabla
            query += "CREATE TABLE " + '{0}'
            query += "(id_'{0}' INT NOT NULL AUTO_INCREMENT, "
        else:
            query += '{value}'
        i += 1
    query += ";"
    return query


def get_slaves_connections():
    """
    Function to get and validate the connection of all the slaves databases.
    """
    # Load the slave connection info from the file.
    slave_connections = json.load(open("connections.json")).get("slave_connections")

    # TODO Use threads
    connections = []
    for connection_data in slave_connections:
        try:
            host = connection_data['host']
            clean_connection_data = connection_data.copy()
            # Remove label
            del clean_connection_data['label']
            conn = create_connection(**clean_connection_data)
            connections.append(conn)
            print(f"[*] Conexión exitosa con el host {host}")
        except:
            print(f"[*] ERROR: Ocurrio un problema al establecer conexión con el host {host}")

    return connections, slave_connections


def create_new_table_query(name, columns: Dict[str, str], relations):
    """
    Function to create the query for create a new table.
    """
    query = "CREATE TABLE " + name + "("
    for column, type in columns.items():
        query += column + " " + type + ", "
    # Add primary key
    query += "sucursal VARCHAR(50),"
    query += "id INT NOT NULL AUTO_INCREMENT, "
    query += "PRIMARY KEY (id));"
    return query

def generate_server_sql(label, host, database, port, user, password):
    """
    Generate a SQL Query to create the spider server.
    """
    query = """
            CREATE OR REPLACE SERVER Server%s FOREIGN DATA WRAPPER mysql
            OPTIONS(HOST '%s', DATABASE '%s', PORT %s,
            USER '%s', PASSWORD '%s');
            """ % (label, host, database, port, user, password)
    return query


def generate_new_table(conn):
    """
    Function to generate a new table based in the input of the user.
    """
    # Get all the slaves db connections
    connections, connections_data = get_slaves_connections()

    # Create SQL for Server connections
    server_queries = []
    for conn_data in connections_data:
        server_queries.append(generate_server_sql(**conn_data))

    # Execute queries to create server connections
    for query in server_queries:
        conn.execute(query)

    # Request the information for the table
    name = input("Ingresa el nombre de la tabla: ")
    total_columns = int(input("Ingresa el total de columnas: "))
    columns = {}
    for i in range(total_columns):
        column_name = input("Ingresa el nombre de la columna: ")
        column_type = input("Ingresa el tipo de dato de la columna: ")
        columns[column_name] = column_type

    # Generate query to create the table
    slave_query = create_new_table_query(name, columns, [])

    # Modify the query to create the table in the master database using spider
    master_query = slave_query[:-1]
    spider_engine = """
    ENGINE=Spider
    COMMENT 'wrapper "mysql", table "%s"'
    PARTITION BY LIST COLUMNS (sucursal) (
    """ % name
    master_query += spider_engine

    # Generate partitions and add them to the master query
    for i, data in enumerate(connections_data):
        partition = """PARTITION p%s VALUES IN ("%s") COMMENT = 'srv "Server%s"',""" % (i, data.get("label").lower(), data.get("label"))
        master_query += partition.strip().strip()
    master_query = master_query[:-1]
    master_query += ");"

    # Apply query in all databases.
    for connection in connections:
        try:
            connection.execute(slave_query)
            print(f"[*] Tabla {name} creada exitosamente en la base de datos {connection.engine.url.database}")
        except:
            print(f"[*] ERROR: Ocurrio un problema al crear la tabla {name} en la base de datos {connection.engine.url.database}")

    master_query = master_query.replace("PRIMARY KEY (id)", "PRIMARY KEY (id, sucursal)")
    # Apply query for master
    conn.execute(master_query)

    # Close connections
    list(map(Connection.close, connections))
    print("Conexiones cerradas con las bases de datos.")


def select_database_location():
    """
    Function to select the city in which you are going to
    perform the operations.
    """
    locations = config.get("LOCATIONS").split(",")
    print("Sucursales disponibles: ")
    for location in locations:
        print("-", location)
    choice = input("Selecciona la ubicacion de tu sucursal: ")
    if choice.lower() not in locations:
        pass
    return unidecode.unidecode(choice.lower())

def list_databases(conn):
    """
    List the available databases in the servers.
    """
    databases = list(zip(*(conn.execute(text("SHOW DATABASES LIKE 'sucursal%';")))))[0]
    # Generate a dict with the key numbers and the databases values.
    databases_options = dict(zip(range(1, len(databases)+1), databases))
    return databases_options

def validate_connection():
    print("Probando conexion a base de datos...")
    # Validate that config has variables
    if not config:
        print("ERROR: Tienes que crear un archivo llamado '.env' y escribir las variables para la conexion.")
        sys.exit()
    else:
        empty_variables = []
        for variable, value in config.items():
            if not value:
                print(f"ERROR: La variable {variable} no tiene un valor asignado")
                empty_variables.append(variable)
        if empty_variables:
            sys.exit()
    try:
        conn = load_main_connection()
        conn.close()
    except sqlalchemy.exc.OperationalError as e:
        print("ERROR: Ocurrio un error con el siguiente detalle:", e.orig)
        sys.exit()

    print("La conexion a la base de datos ha sido exitosa")

OPTIONS = {
    "0": act.list_users,
    "1": act.search_user,
    "2": act.create_user,
    "3": act.update_user,
    "4": act.list_address,
    "5": act.create_direccion,
    "6": act.update_direccion,
    "7": generate_new_table
}


if __name__ == "__main__":
    # Test the connection to the database
    validate_connection()

    conn = load_main_connection()

    print_menu()
    finished = False

    while not finished:
        try:
            user_choice = input("\nElige que quieres realizar: ")
            query_generator = OPTIONS.get(user_choice) #["1"] # OPTIONS.get("1")
            if user_choice == 'X': #Exit
                finished = True
            elif not query_generator:
                print("La opcion no es valida, introduce una accion correcta")
                continue
            else:
                query_generator(conn)
        except KeyboardInterrupt:
            print()
            sys.exit()



    conn.close()
