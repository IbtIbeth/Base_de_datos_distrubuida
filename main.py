from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy import text
import sqlalchemy
from dotenv import dotenv_values
import sys
import actions as act
import unidecode
import json


config = dotenv_values(".env")# take environment variables from .env.


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

def generate_new_table(conn):
    
    # Get all the slaves db connections

    # Create the slaves db connections

    # 

    create_new_table_query()



def create_new_table_query(name, columns: Dict[str, str], relations):
    pass


OPTIONS = {
    "0": act.list_users,
    "1": act.search_user,
    "2": act.create_user,
    "3": act.update_user,
    "4": act.list_address,
    "5": act.create_direccion,
    "7": generate_new_table
}

def load_main_connection():
    #Validate the location is valid...+
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
            conn = create_connection(**connection_data)
            connections.append(conn)
            print(f"[*] Conexión exitosa con el host {host}")
        except:
            print(f"[*] ERROR: Ocurrio un problema al establecer conexión con el host {host}")
    # breakpoint()
    # Validate each connection
    return connections


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
