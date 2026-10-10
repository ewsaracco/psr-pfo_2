from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
DB_NAME = "tareas.db"

def init_db():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contraseña = datos.get('contraseña')

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    password_hasheada = generate_password_hash(contraseña)

    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", (usuario, password_hasheada))
        conexion.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    finally:
        conexion.close()

@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contraseña = datos.get('contraseña')

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado and check_password_hash(resultado[0], contraseña):
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    # Devolvemos un HTML simple como pide la consigna
    return "<h1>Bienvenido al sistema de Gestión de Tareas</h1><p>API REST funcionando correctamente.</p>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)