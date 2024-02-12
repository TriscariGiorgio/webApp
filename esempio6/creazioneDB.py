from funzioniDB import *

if __name__ == '__main__':
    pw = ""
    db = "museo"
    connection = create_server_connection("localhost", "root", pw)
    create_database(connection, "CREATE DATABASE museo")
    connection = create_db_connection("localhost", "root", pw, db)
    query = """SET GLOBAL max_allowed_packet = 268435456"""
    cursor = connection.cursor()
    cursor.execute(query)