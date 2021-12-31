from sqlalchemy import text



def list_users(conn):
    query = "SELECT * FROM CLIENTE;"
    res = conn.execute(query)
    # Show the users
    for user_data in res:
        print(*user_data)



def search_user(conn):
    """
    Function to search a user in the database using its info like
    RFC, name, and address
    """
    print("* Seleccione el parametro de búsqueda:")
    print("[1] Nombre/s")
    print("[2] Apellido paterno")
    print("[3] Apellido materno")
    print("[4] RFC")
    print("[5] Dirección")
    option = input()
    while option not in "12345":
        print("Opcion no válida. Introduce un valor válido. ")
        option = input()

    search_parameter = input("Introduce el texto de búsqueda: ")

    if option == "1":
        condition = f'nombre="{search_parameter}"'
    elif option == "2":
        condition = f'apellido_paterno="{search_parameter}"'
    elif option == "3":
        condition = f'apellido_materno="{search_parameter}"'
    elif option == "4":
        condition = f'rfc="{search_parameter}"'
    # elif option == "5": # TODO Add later
    #     condition = f"direccion={search_parameter}"

    # TODO Find a better way to select the table
    query = "SELECT * FROM CLIENTE WHERE " + condition + ";"
    breakpoint()
    res = list(conn.execute(text(query)))
    breakpoint()
    if res:
        for user_data in res:
            print(*user_data)
    else:
        print("No se encontró el cliente")



def create_user(conn):
    """
    Function to create a user in the database
    """
    from main import select_database_location
    print("* Complete los siguientes campos:")
    nombre = input("Nombre: ")
    apellido_paterno = input("Apellido paterno: ")
    apellido_materno = input("Apellido materno: ")
    rfc = input("RFC: ")
    sucursal = select_database_location()
    while not sucursal:
        print("Error. Escoge una sucursal válida.")
        sucursal = select_database_location()

    query = 'INSERT INTO CLIENTE (nombre, apellido_paterno, apellido_materno, rfc, sucursal) VALUES("%s", "%s", "%s", "%s", "%s")' %(nombre, apellido_paterno, apellido_materno, rfc, sucursal)
    query += ";"
    conn.execute(query)


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


def list_address(conn):
    query = "SELECT * FROM DIRECCION;"
    res = conn.execute(query)
    # Show addresses
    for address_data in res:
        print(*address_data)


def create_direccion(conn):
    from main import select_database_location
    print("* Complete los siguientes campos:")
    calle = input("Calle: ")
    numero = input("Número: ")
    colonia=input("Colonia: ")
    ciudad = input("Ciudad: ")
    estado = input("Estado: ")
    cp = input("Código postal: ")
    sucursal = select_database_location()
    while not sucursal:
        print("Error. Escoge una sucursal válida.")
        sucursal = select_database_location()

    query = 'INSERT INTO DIRECCION (calle, numero, colonia, ciudad, estado, cp, sucursal) VALUES("%s", "%s", "%s", "%s", "%s", %s, "%s")' %(calle, numero, colonia, ciudad, estado, cp, sucursal)
    query += ";"
    conn.execute(query)

    """
    Function to create a user in the database
    """
    '''calle, numero, colonia, estado, cp = input("Introduce el calle, numero, colonia, estado y código postal separados por espacios: ").split()


def update_direccion(id_direccion, id_cliente):
    query = "UPDATE direccion SET id_direccion = %s, id_cliente = %s " %(id_direccion, id_cliente)
    query += " WHERE "
    query += "{}='{}'".format(key, value)
    query += ";"
    return query
'''
