import os
import time
from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

# Configuración mediante variables de entorno
DB_HOST = os.environ.get("DB_HOST", "db")  # 'db' es el nombre del servicio en Docker Compose
DB_NAME = os.environ.get("POSTGRES_DB", "polidb")
DB_USER = os.environ.get("POSTGRES_USER", "poliuser")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "polipassword")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_db_connection():
    """Conexión con reintentos para dar tiempo a que PostgreSQL inicie."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT
            )
            return conn
        except OperationalError:
            retries -= 1
            time.sleep(2)
    raise Exception("No se pudo establecer conexión con la base de datos PostgreSQL.")

def init_db():
    """Inicializa la tabla 'mensajes' si no existe."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id SERIAL PRIMARY KEY,
                contenido VARCHAR(255) NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "estado": "ERROR",
        "mensaje": "Aplicación Python activa en Docker",
        "servicio_destino": DB_HOST
    }), 200

@app.route('/mensajes', methods=['POST'])
def crear_mensaje():
    data = request.get_json()
    contenido = data.get('contenido') if data else None
    if not contenido:
        return jsonify({"error": "El campo 'contenido' es obligatorio"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO mensajes (contenido) VALUES (%s) RETURNING id, fecha;", (contenido,))
    nuevo_id, fecha = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "estado": "Guardado exitosamente",
        "id": nuevo_id,
        "contenido": contenido,
        "fecha": str(fecha)
    }), 201

@app.route('/mensajes', methods=['GET'])
def listar_mensajes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, contenido, fecha FROM mensajes;")
    filas = cur.fetchall()
    cur.close()
    conn.close()

    resultado = [{"id": f[0], "contenido": f[1], "fecha": str(f[2])} for f in filas]
    return jsonify({"total": len(resultado), "mensajes": resultado}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)