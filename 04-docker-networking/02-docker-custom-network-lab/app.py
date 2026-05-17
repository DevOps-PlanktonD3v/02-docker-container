import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", 5432),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", "postgres"),
    "dbname": os.environ.get("DB_NAME", "postgres"),
}


@app.route("/")
def index():
    return jsonify({
        "app": "flask-networking-lab",
        "message": "Docker Networking Lab - Flask + PostgreSQL",
        "endpoints": ["/", "/health", "/db-check"],
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/db-check")
def db_check():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({
            "status": "connected",
            "db_host": DB_CONFIG["host"],
            "db_port": DB_CONFIG["port"],
            "db_name": DB_CONFIG["dbname"],
            "pg_version": version,
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "db_host": DB_CONFIG["host"],
            "db_port": DB_CONFIG["port"],
            "db_name": DB_CONFIG["dbname"],
            "error": str(e),
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
