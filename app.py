from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Conexión a la base de datos
def crear_conexion():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='appcrud',
            user='root',
            password='root'  # Cambia esta contraseña si es diferente
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None

# Ruta principal (Listar usuarios)
@app.route('/')
def index():
    connection = crear_conexion()
    if connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        connection.close()
        return render_template('index.html', usuarios=usuarios)
    return "Error al conectarse a la base de datos."

# Ruta para agregar un usuario
@app.route('/agregar', methods=['POST'])
def agregar_usuario():
    nombre = request.form['nombre']
    edad = request.form['edad']
    connection = crear_conexion()
    if connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, edad) VALUES (%s, %s)', (nombre, edad))
        connection.commit()
        connection.close()
    return redirect('/')

# Ruta para eliminar un usuario
@app.route('/eliminar/<int:user_id>', methods=['POST'])
def eliminar_usuario(user_id):
    connection = crear_conexion()
    if connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (user_id,))
        connection.commit()
        connection.close()
    return redirect('/')

# Ruta para editar un usuario
@app.route('/editar/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE usuarios SET nombre = %s, edad = %s WHERE id = %s', (nombre, edad, user_id))
            connection.commit()
            connection.close()
        return redirect('/')
    else:
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
            usuario = cursor.fetchone()
            connection.close()
            return render_template('editar.html', usuario=usuario)
        return "Error al conectarse a la base de datos."

if __name__ == '__main__':
    app.run(debug=True)
