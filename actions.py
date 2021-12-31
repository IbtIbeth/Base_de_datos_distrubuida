from sqlalchemy import text


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
    print("* Seleccione el parametro de búsqueda:")
    print("[1] Nombre o apellidos")
    print("[2] RFC")
    print("[3] Dirección")
    option = input()
    while option not in "123":
        print("Opcion no válida. Introduce un valor válido. ")
        option = input()

    search_parameter = input("Introduce el texto de búsqueda: ")

    if option == "1":
        condition = f'nombre="{search_parameter}" OR apellido_paterno="{search_parameter}" OR apellido_materno="{search_parameter}"'
    elif option == "2":
        condition = f'rfc="{search_parameter}"'
    # elif option == "3": # TODO Add later
    #     condition = f"direccion={search_parameter}"

    # TODO Find a better way to select the table
    query = "SELECT * FROM CLIENTE WHERE " + condition + ";"
    res = list(conn.execute(text(query)))
    if res:
        for user_data in res:
            print(*user_data)
    else:
        print("No se encontró el cliente")



def create_user():
    """
    Function to create a user in the database
    """
    nombre, apellido_paterno, apellido_materno, rfc = input("Introduce el nombre, apellido paterno, apellido materno y rfc separados por espacios: ").split()
    query = 'INSERT INTO CLIENTE (nombre, apellido_paterno, apellido_materno, rfc) VALUES("%s", "%s", "%s", "%s")' %(nombre, apellido_paterno, apellido_materno, rfc)
    query += ";"
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

