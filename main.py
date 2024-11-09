from flask import Flask, render_template, request, redirect, url_for,session
import pymysql
import pymysql.cursors
from dbconfig import getDBConnection

app = Flask(__name__)
app.secret_key = "super secret key"
@app.route('/', methods=['GET'])
def home():
    return render_template('sign_in.html')

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        email = request.form['email']

        connection = getDBConnection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM usuarios WHERE email =%s", (email))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return render_template('sign_in.html', message="El email ya ha sido registrado.")

        try:
            cursor.execute("INSERT INTO usuarios (usuario, contraseña, email) VALUES (%s,%s,%s)", (usuario, contraseña, email))
            connection.commit()
            return redirect(url_for('login'))
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

    return render_template('sign_in.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
    
        connection = getDBConnection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND contraseña = %s", (email, contraseña))
        usuario_existente = cursor.fetchone()
        cursor.close()

        if usuario_existente is not None:
            session['email'] = email
            session['usuario'] = usuario_existente['usuario']

            return redirect(url_for('index'))
        else:
            return render_template('login.html', message="Correo o constraseña incorrectos")

    return render_template('login.html')

@app.route('/form', methods=["GET"])
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

    return render_template('form.html', musica = registro, musica_to_edit=None)

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
    connection = getDBConnection()
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
    return render_template('edit.html', musica =[], musica_to_edit=contact)

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
    app.run(debug=True, host="0.0.0.0")