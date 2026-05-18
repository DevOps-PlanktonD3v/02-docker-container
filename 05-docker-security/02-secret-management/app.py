import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_password() -> str:
    """
    Resolve database password with priority:
    1. Docker Secret file (DB_PASSWORD_FILE)
    2. Environment variable (DB_PASSWORD)
    """
    secret_file = os.environ.get("DB_PASSWORD_FILE")
    if secret_file:
        try:
            with open(secret_file, "r") as f:
                return f.read().strip()
        except (OSError, IOError) as e:
            raise RuntimeError(f"Failed to read secret file '{secret_file}': {e}")

    password = os.environ.get("DB_PASSWORD")
    if password:
        return password

    raise RuntimeError(
        "Database password not found. "
        "Set DB_PASSWORD_FILE (Docker Secret) or DB_PASSWORD (env var)."
    )


def get_db_config() -> dict:
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "postgres"),
        "password": get_db_password(),
        "dbname": os.environ.get("DB_NAME", "postgres"),
    }


def connect_db():
    config = get_db_config()
    return psycopg2.connect(**config, connect_timeout=5)


@app.route("/")
def index():
    secret_method = (
        "docker_secret" if os.environ.get("DB_PASSWORD_FILE") else "env_var"
    )
    return jsonify(
        {
            "app": "Flask Secret Management Demo",
            "secret_method": secret_method,
            "endpoints": ["/", "/health", "/db-check"],
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/db-check")
def db_check():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()

        secret_method = (
            "docker_secret" if os.environ.get("DB_PASSWORD_FILE") else "env_var"
        )
        return jsonify(
            {
                "status": "connected",
                "secret_method": secret_method,
                "db_host": os.environ.get("DB_HOST", "localhost"),
                "db_name": os.environ.get("DB_NAME", "postgres"),
                "db_user": os.environ.get("DB_USER", "postgres"),
                "postgres_version": version,
            }
        )
    except RuntimeError as e:
        return jsonify({"status": "error", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
