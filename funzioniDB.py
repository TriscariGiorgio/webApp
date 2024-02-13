import mysql.connector
from mysql.connector import Error


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection



def esegui_query(connection, query, more=False):
    cursor = connection.cursor()
    try:
        cursor.execute(query, multi=more)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def esegui_query_2(connection, query, more=False):
    cursor = connection.cursor()
    try:
        cursor.executemany(None, query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def esegui_query_many(connection, query, dati):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, dati)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def inserisci_dati(connection, tabella, lista, campi=None):
    cursor = connection.cursor()
    try:
        if campi:
            cursor.executemany(f"INSERT INTO {tabella} ({','.join(campi)}) VALUES ({','.join(['%s'] * len(campi))})",
                               lista)
            connection.commit()
        else:
            esegui_query_many(connection, f"INSERT INTO {tabella}  VALUES ({','.join(['%s'] * len(lista[0]))})", lista)
            connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def modifica_dati(connection, tabella, colonna, valore, condizione=None):
    cursor = connection.cursor()
    try:
        if condizione:
            cursor.executemany(f"UPDATE {tabella} SET {colonna}={valore} WHERE {condizione}", valore)
            connection.commit()
        else:
            cursor.executemany(f"UPDATE {tabella} SET {colonna}={valore}", valore)
            connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def elimina_dati(connection, tabella, colonna, condizione=None):
    cursor = connection.cursor()
    try:
        if condizione:
            cursor.execute(f"DELETE FROM {tabella} WHERE {colonna}={condizione}")
            connection.commit()
        else:
            cursor.execute(f"DELETE FROM {tabella}")
            connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def menu(connection):
    while True:
        lista_operazioni = [1, 2, 3, 4]
        menu = int(input("inserire cosa si vuole effettuare: 1.aggiungere dati a tabella\n\t\t\t\
                2.Modificare dati di una tabella \n\t\t\t\t\t\t\t 3.Eliminare dati di una tabella\
                4.per uscire"))
        if menu not in lista_operazioni:
            raise ValueError("iserire un operazione valida")

        if menu == 1:
            tabelle_disponibili = [tabella[0] for tabella in read_query(connection, "SHOW TABLES;")]
            tabella = input(f"in che tabella si vogliono inserire i dati:{tabelle_disponibili} disponibili")
            colonne_tabella = read_query(connection, f"SHOW COLUMNS FROM {tabella}")
            lista_valori = []
            for colonna in colonne_tabella:
                valore = input(f"che valore vuoi inserire nella colonna {colonna}:")
                lista_valori.append(valore)
            colonne_tabella2 = [colonna[0] for colonna in colonne_tabella]

            lista_valori = [tuple(lista_valori)]

            inserisci_dati(connection, tabella, lista_valori, colonne_tabella2)

        if menu == 2:
            tabelle_disponibili = [tabella[0] for tabella in read_query(connection, "SHOW TABLES;")]
            tabella = input(f"in che tabella si vogliono modificare i dati:{tabelle_disponibili} disponibili")
            colonne_tabella = [colonna[0] for colonna in read_query(connection, f"SHOW COLUMNS FROM {tabella}")]
            colonna = input(f"inserire la colonna da voler modificare:{colonne_tabella} disponibili")
            valore = input("valore da inserire")
            condizione = int(input("inserire 1 per modificare tutta la colonna o 2 per condizione: "))
            if condizione == 1:
                modifica_dati(connection, tabella, colonna, valore)
            elif condizione == 2:
                condizione = input("iserire condizione: ")
                modifica_dati(connection, tabella, colonna, valore, condizione)

        if menu == 3:
            tabelle_disponibili = [tabella[0] for tabella in read_query(connection, "SHOW TABLES;")]
            tabella = input(f"di che tabella si vogliono eliminare i dati:{tabelle_disponibili} disponibili")
            eliminare_colonna = int(input(
                "inserire 1 se si vuole eliminare tutta la tabella, 2 se si vuole eliminare tutti i dati della tabella, 3 se si vuole eliminare dalla colonna"))
            if eliminare_colonna == 1:
                esegui_query(connection, f"DROP TABLE {tabella}")
            elif eliminare_colonna == 2:
                colonne_tabella = [colonna[0] for colonna in read_query(connection, f"SHOW COLUMNS FROM {tabella}")]
                colonna = input(f"inserire una colonna tra:{colonne_tabella} disponibili")
                esegui_query(connection, f"DELETE FROM {tabella} WHERE {colonna}")
            elif eliminare_colonna == 3:
                colonne_tabella = [colonna[0] for colonna in read_query(connection, f"SHOW COLUMNS FROM {tabella}")]
                colonna = input(f"inserire la colonna da voler modificare:{colonne_tabella} disponibili")
                condizione = input("iserire la condizione per eliminare le righe")
                elimina_dati(connection, tabella, colonna, condizione)

        else:
            break
