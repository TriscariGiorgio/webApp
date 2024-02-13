from funzioniDB import *
import csv

if __name__ == '__main__':
    pw = ""
    db = "museo"
    connection = create_server_connection("localhost", "root", pw)
    esegui_query(connection, "DROP DATABASE museo")
    create_database(connection, "CREATE DATABASE museo")
    connection = create_db_connection("localhost", "root", pw, db)
    query = """SET GLOBAL max_allowed_packet = 268435456"""
    cursor = connection.cursor()
    cursor.execute(query)

    esegui_query(connection, """
        CREATE TABLE IF NOT EXISTS `artista` (
        `id` INT(11) PRIMARY KEY ,
        `name` VARCHAR(255),
        `nazionalita`  VARCHAR(255)
    );
    """)
    esegui_query(connection, """
        CREATE TABLE IF NOT EXISTS `opera` (
        `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
        `titolo` VARCHAR(255),
        `thumbnail`  VARCHAR(255),
        `anno` int(11),
        `id_artista` INT(11)
    );
    """)
    esegui_query(connection, """
    ALTER TABLE `opera` 
      ADD CONSTRAINT `opera_ibfk_1` FOREIGN KEY (`id_artista`) REFERENCES `artista` (`id`);
    """)

    with open(r"C:\webApp\Artisti_pulito.csv", encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        reader = list(reader)


    lista_campi_artista = ["id","name", "nazionalita"]
    lista_artisti = []
    diz_artisti={}
    for i in range(len(reader)):
        lista_artisti.append((i, reader[i][2], reader[i][1]))
        diz_artisti[reader[i][2]]=i

    with open(r"C:\webApp\unione..csv", encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        reader = list(reader)

    lista_campi_opera=["titolo","thumbnail","anno","id_artista"]
    lista_opere=[]
    for i in range(100):
        lista_opere.append((reader[i][1], reader[i][4], reader[i][3],diz_artisti[reader[i][2]]))

    inserisci_dati(connection, "artista", lista_artisti)
    inserisci_dati(connection, "opera", lista_opere, lista_campi_opera)

