from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pymysql.cursors
from dbconfig import getDBConnection

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id, cancion, album, artista, genero, rating FROM musica")
        registro = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        registro = []
    finally:
        cursor.close()
        connection.close()

    return render_template('form.html', musica = registro, music_to_edit=None)

@app.route('/', methods=['POST'])
def submit():
    cancion = request.form['cancion']
    album = request.form['album']
    artista = request.form['artista']
    genero = request.form['genero']
    rating = request.form['rating']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO musica (cancion, album, artista, genero, rating) VALUES (%s,%s,%s,%s,%s)", (cancion, album, artista, genero, rating))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

@app.route('/edit/<int:musica_id>',methods=['GET'])
def edit(musica_id):
    connection = getDBConnection
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id,cancion, album, artista, genero, rating FROM musica WHERE id=%s",(musica_id))
        contact = cursor.fetchone()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        contact = None
    finally:
        cursor.close()
        connection.close()
    return render_template('edit_musica.html', musica =[], musica_to_edit=contact)

@app.route('/update/<int:musica_id>', methods =['POST'])
def update(musica_id):
    cancion = request.form['cancion']
    album = request.form['album']
    artista = request.form['artista']
    genero = request.form['genero']
    rating = request.form['rating']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE musica SET cancion = %s, album = %s, artista = %s, genero = %s, rating = %s WHERE id=%s ", (cancion, album, artista, genero, rating,musica_id))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:musica_id>', methods=['POST'])
def delete(musica_id):
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM musica WHERE id=%s", (musica_id))
        connection.commit()
    except pymysql.MySQLError as e: 
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True)