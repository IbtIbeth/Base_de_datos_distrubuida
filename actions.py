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


def update_user(conn):
    user_id = input("Introduce el ID del usuario que quieres actualizar: ")
    updatable_fields = ["nombre", "apellido_paterno", "apellido_materno", "rfc", "sucursal"]
    query = update_values_from_row(user_id, "CLIENTE", updatable_fields)

    # Update user
    conn.execute(text(query))
    print(f"Se actualizó correctamente el usuario con ID {user_id}")



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


def update_direccion(id_direccion, id_cliente):
    query = "UPDATE direccion SET id_direccion = %s, id_cliente = %s " %(id_direccion, id_cliente)
    query += " WHERE "
    query += "{}='{}'".format(key, value)
    query += ";"
    return query


def update_values_from_row(table_id, table, updatable_fields: list):
    query = f"UPDATE {table}"
    print("Introduce el valor por el que lo quieres actualizar, si quieres mantenerlo igual solo omitelo presionando la tecla ENTER")
    new_fields = {}
    for field in updatable_fields:
        new_value = input(f'Introduce el nuevo valor {field.replace("_", " ")}: ')
        if new_value:
            new_fields[field] = new_value
    updates = " SET"
    for column, value in new_fields.items():
        updates += f" {column}='{value}',"

    condition = f" WHERE id={table_id}"
    query = query + updates[:-1] + condition + ";"
    return query
