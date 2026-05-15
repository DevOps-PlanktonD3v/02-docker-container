import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "flask-app")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
PORT = int(os.getenv("PORT", 5000))


@app.route("/")
def index():
    return jsonify({
        "app": APP_NAME,
        "env": APP_ENV,
        "version": APP_VERSION,
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/env")
def env():
    return jsonify({
        "APP_NAME": APP_NAME,
        "APP_ENV": APP_ENV,
        "APP_VERSION": APP_VERSION,
        "PORT": PORT,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
