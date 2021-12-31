from sqlalchemy import create_engine, exc
from sqlalchemy import text
import sqlalchemy
from sqlalchemy.sql.functions import user
import os
from dotenv import dotenv_values
import sys

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
    print("[1] - Buscar usuario por RFC, Nombre o Domicilio")
    print("[2] - Crear usuario")
    print("[3] - Actualizar usuario")
    print("[4] - Crear dirección")
    print("[5] - Actualizar dirección")
    print("[6] - Crear tabla")


# def execute_query(func):
#     def wrapper(conn, *args, **kwargs):

#         result = func()
#         conn.close()
#         return result

#     return wrapper

def list_users(conn):
    query = "SELECT * FROM CLIENTE;"
    res = conn.execute(query)
    # Show the users
    for user_data in res:
        print(*user_data)
    conn.close()



def search_user(conn):
    """
    Function to search a user in the database using its info like
    RFC, name, and address
    """
    #print("* Para buscar al cliente, por RFC, utilice el siguiente formato: rfc = 'inserte el rfc entre comillas'")
    # print("* Para buscar al cliente, por nombre, utilice el siguiente formato: nombre = 'inserte el nombre entre comillas'")
    # TODO Validate search for address
    #print("* Para buscar al cliente, por domicilio, utilice el siguiente formato: ")
    print("* Seleccione el parametro de busqueda:")
    print("[1] Nombre o apellidos")
    print("[2] RFC")
    print("[3] Dirección")
    option = input()
    while option not in "123":
        print("Opcion no valida. Introduce un valor valido. ")
        option = input()

    search_parameter = input("Introduce el texto de busqueda: ")

    if option == "1":
        condition = f'nombre="{search_parameter}" OR apellido_paterno="{search_parameter}" OR apellido_materno="{search_parameter}"'
    elif option == "2":
        condition = f'rfc="{search_parameter}"'
    # elif option == "3": # TODO Add later
    #     condition = f"direccion={search_parameter}"

    # TODO Find a better way to select the table
    query = "SELECT * FROM CLIENTE WHERE " + condition + ";"
    breakpoint()
    res = conn.execute(text(query))
    for user_data in res:
        print(*user_data)

    # i = 0
    # breakpoint()
    # for key, value in kwargs.items():
    #     if i == 0:
    #         query += " WHERE "
    #     else:
    #         query += " AND "
    #     query += "{}='{}'".format(key, value)
    #     i += 1
    # query += ";"
    #conn.close()


def create_user():
    """
    Function to create a user in the database
    """
    nombre, apellido_paterno, apellido_materno, rfc = input("Introduce el nombre, apellido paterno, apellido materno y rfc separados por espacios: ").split()
    query = 'INSERT INTO CLIENTE (nombre, apellido_paterno, apellido_materno, rfc) VALUES("%s", "%s", "%s", "%s")' %(nombre, apellido_paterno, apellido_materno, rfc)
    query += ";"
    # breakpoint()
    return query

def update_user():
    nombre, apellido_paterno, apellido_materno, rfc = input("Introduce el nombre, apellido paterno, apellido materno separado por espacios: ").split()
    id_cliente = search_user(nombre, apellido_paterno, apellido_materno)
    print("[1] - Nombre")
    print("[2] - Apellido paterno")
    print("[3] - Apellido materno")
    print("[4] - RFC")
    options = {'1' : 'nombre', '2': 'apellido_paterno', '3': 'apellido_materno', '4': 'rfc'}
    changes = input("Introduce los números de los campos en los que quieras realizar cambios, separados por espacios: ").split()
    query = "UPDATE CLIENTE "
    i = 0
    for j in changes:
        new_val = input("Introduce el nuevo valor del ") + str(options[j])
        while(i == 0):
            query += "SET "
        else:
            query += " AND "
        query += str(options[j]) + " = '" + str(new_val[j]) + "'"
        i += 1

    query += " WHERE id_cliente = '" + str(id_cliente) +"';"
    return query

def create_direccion(calle, numero, colonia, estado, cp ):
    """
    Function to create a user in the database
    """
    calle, numero, colonia, estado, cp = input("Introduce el calle, numero, colonia, estado y código postal separados por espacios: ").split()
    query = "INSERT INTO direccion (calle, numero, colonia, estado, cp) VALUES(%s, %s, %s, %s, %s)" %(calle, numero, colonia, estado, cp)
    query += ";"
    return query

def update_direccion(id_direccion, id_cliente):
    query = "UPDATE direccion SET id_direccion = %s, id_cliente = %s " %(id_direccion, id_cliente)
    query += " WHERE "
    query += "{}='{}'".format(key, value)
    query += ";"
    return query

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
    pass


OPTIONS = {
    "0": list_users,
    "1": search_user,
    "2": create_user,
}

def create_connection():
    #Validate the location is valid...+
    database = config.get("DATABASE")
    user = config.get("USER_DB")
    password = config.get("PASSWORD")
    host = config.get("HOST")
    port = config.get("PORT")
    #database = "patzcuaro"
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')


    #TODO Handle error in connection
    return engine.connect()

def list_databases(conn):
    """
    List the available databases in the servers.
    """
    databases = list(zip(*(conn.execute(text("SHOW DATABASES LIKE 'sucursal%';")))))[0]
    # Generate a dict with the key numbers and the databases values.
    databases_options = dict(zip(range(1, len(databases)+1), databases))
    return databases_options


def select_database():
    pass


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
        conn = create_connection()
        conn.close()
    except sqlalchemy.exc.OperationalError as e:
        print("ERROR: Ocurrio un error con el siguiente detalle:", e.orig)
        sys.exit()

    print("La conexion a la base de datos ha sido exitosa")

def select_database_location():
    """
    Function to select the city in which you are going to
    perform the operations.
    """
    locations = config.get("LOCATIONS")
    print("Sucursales disponibles: ")
    for location in locations:
        print("-", location)
    choice = input("Selecciona la ubicacion de tu sucursal: ")
    if choice.lower() not in locations:
        pass
    return choice 


if __name__ == "__main__":
    # Test the connection to the database
    validate_connection()

    conn = create_connection()


    print_menu()
    finished = False
    
    while not finished:
        user_choice = input("\nElige que quieres realizar: ")
        query_generator = OPTIONS.get(user_choice) #["1"] # OPTIONS.get("1")
        if not query_generator:
            print("La opcion no es valida, introduce una accion correcta")
            continue
        else:
            query_generator(conn)

    conn.close()
