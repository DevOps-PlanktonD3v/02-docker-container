import os
from flask import Flask, jsonify

app = Flask(__name__)

PORT = int(os.getenv("PORT", 5000))


@app.route("/")
def index():
    return jsonify({
        "app": "flask-healthcheck",
        "status": "running",
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
