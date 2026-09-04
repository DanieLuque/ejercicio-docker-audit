import logging
import os
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "legacydb")


@app.route("/")
def home():
    try:
        import pymysql
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            connect_timeout=5,
        )
        conn.close()
        return "<h1>API Legacy - Funcionando</h1>"
    except Exception as e:
        logger.exception("Error conectando a la base de datos")
        return "<h1>Sistema Caído</h1>", 500


@app.route("/buscar")
def buscar_usuario():
    try:
        usuario_id = int(request.args.get("id", "1"))
    except ValueError:
        return "<h1>Parámetro inválido</h1>", 400

    query = "SELECT * FROM usuarios WHERE id = %s"
    return f"Simulando consulta parametrizada: {query} (id={usuario_id})"


@app.route("/health")
def health_check():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
