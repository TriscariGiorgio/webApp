import json
from funzioniDB import *
from flask import Flask, jsonify, render_template, request, redirect, url_for
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
    query = """SELECT o.titolo, o.anno, o.thumbnail,o.id_artista, a.name, a.nazionalita 
            FROM opera  o
            JOIN artista  a
            ON o.id_artista = a.id;
        """
    items = execute_query(query)
    return items
    # return jsonify({'items': items})

@app.route('/data/artisti', methods=['GET'])
def get_data_artisti():
    query = "SELECT * FROM artista"
    items = execute_query(query)
    return items


@app.route('/data/opere/name/<name>', methods=['GET'])
def get_opera_by_artista_id(name):
    query = """
        SELECT *
        FROM opera o
        JOIN artista a
        ON o.id_artista = a.id
        WHERE a.name = %s;
    """
    opere = execute_query(query, (name,))
    # return jsonify({'opere': opere})
    return opere


@app.route('/opere')
def show_opere():
    opere = get_data_opere()
    return render_template('opere.html', opere=opere)


@app.route('/artisti')
def show_artisti():
    artisti = get_data_artisti()
    return render_template('artisti.html', artisti=artisti)

@app.route('/artisti/artista/<name>')
def show_artista(name):
    artista = get_opera_by_artista_id(name)
    return render_template('artista.html', artista=artista)


@app.route('/')
def home():
    return render_template('home.html')


# Route per creare una nuova opera
@app.route('/inserisci_artista', methods=['POST'])
def inserisci_artista():
    nome = request.form['nome']
    nazionalita = request.form['nazionalita']
    query = "INSERT INTO opera (titolo, anno, thumbnail, nome_artista) VALUES ( %s, %s)"
    params = (nome,nazionalita)
    esegui_query(query, params)
    # Qui puoi inserire la logica per salvare i dati nel database

    return "ok"


@app.route('/aggiungi_opera/<int:artista_id>', methods=[ 'POST'])
def aggiungi_opera(artista_id):
    if request.method == 'POST':
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']
        anno = request.form['anno']
        tipo = request.form['tipo']

        # Qui puoi inserire la logica per salvare i dettagli dell'opera nel database

        return 'ok'


@app.route('/data/opere', methods=['POST'])
def create_opera():
    data = request.json
    query = "INSERT INTO opera (titolo, anno, thumbnail, nome_artista) VALUES (%s, %s, %s, %s)"
    params = (data['titolo'], data['anno'], data['thumbnail'], data['nome_artista'])
    esegui_query(query, params)
    return jsonify({'message': 'Opera creata con successo'}), 201


@app.route('/data/opere/<int:id>', methods=['PUT'])
def update_opera(id):
    data = request.json
    query = "UPDATE opera SET titolo = %s, anno = %s, thumbnail = %s, nome_artista = %s WHERE id = %s"
    params = (data['titolo'], data['anno'], data['thumbnail'], data['nome_artista'], id)
    execute_query(query, params)
    return jsonify({'message': 'Opera aggiornata con successo'})

# Route per cancellare una singola opera
@app.route('/data/opere/<int:id>', methods=['DELETE'])
def delete_opera(id):
    query = "DELETE FROM opera WHERE id = %s"
    execute_query(query, (id,))
    return jsonify({'message': 'Opera eliminata con successo'})
if __name__ == '__main__':
    app.run(debug=True)
