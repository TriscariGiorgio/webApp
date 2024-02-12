import json
from funzioniDB import *
from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configura la connessione al database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'museo'
}


# Funzione per creare una connessione al database
def create_db_connection():
    return mysql.connector.connect(**db_config)


# Funzione per eseguire query SQL
def execute_query(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


# Rotte dell'API
@app.route('/data/opere', methods=['GET'])
def get_data_opere():
    query = """SELECT o.titolo, o.anno, o.thumbnail,o.nome_artista, a.name, a.nazionalita 
            FROM opera  o
            JOIN artista  a
            ON o.nome_artista = a.name;
        """
    items = execute_query(query)
    return items
    # return jsonify({'items': items})


@app.route('/data/artisti', methods=['GET'])
def get_data_artisti():
    query = "SELECT * FROM artista"
    items = execute_query(query)
    return items


# singolo show in base all'id passato
@app.route('/data/artisti/<int:id>', methods=['GET'])
def get_singleartista_data(id):
    query = "SELECT * FROM artista WHERE name = %s"
    shows = execute_query(query, (id,))
    return jsonify({'shows': shows})


# @app.route('/data/shows/category/<category_name>', methods=['GET'])
# def get_artista_by_opera(category_name):
#     query = """
#         SELECT opera.titolo, opera.data, opera.tumbnail, artista.nome, artista.nazionalita
#         FROM opera
#         JOIN artista
#         ON opera.id_artista = artista.id_artista;
#     """
#     shows = execute_query(query, (category_name,))
#     return jsonify({'shows': shows})


@app.route('/data/opere/id/<id_artista>', methods=['GET'])
def get_opera_by_artista_id(category_id):
    query = """
        SELECT o.titolo, o.anno, o.thumbnail, a.name, a.nazionalita 
        FROM opera o
        JOIN artista a
        ON o.nome_artista = a.name;
    """
    shows = execute_query(query, (category_id,))
    return jsonify({'shows': shows})
    # return shows


@app.route('/opere')
def show_opere():
    opere = get_data_opere()
    return render_template('opere.html', opere=opere)


@app.route('/artisti')
def show_artisti():
    artisti = get_data_artisti()
    return render_template('artisti.html', artisti=artisti)


@app.route('/opere/artisti/<int:id_artista>')
def show_artista_by_opera(category_id):
    # Recupera tutti i film associati alla categoria specificata
    shows_data_response = get_opera_by_artista_id(category_id)
    # Carica il contenuto JSON come un dizionario Python
    data = json.loads(shows_data_response.get_data(as_text=True))

    # Estrai la lista di show
    movies = data['nome']
    return render_template('tutto.html', movies=movies)


# Funzione per ottenere il nome della categoria
def get_category_name(category_id):
    pass


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
