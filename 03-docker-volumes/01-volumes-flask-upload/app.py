import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

PORT = int(os.getenv("PORT", 5000))
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/app/uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return jsonify({
        "app": "docker-storage-lab",
        "upload_folder": UPLOAD_FOLDER,
        "endpoints": {
            "GET /": "app info",
            "GET /health": "health check",
            "POST /upload": "upload a file",
            "GET /files": "list uploaded files",
        },
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "upload_folder": UPLOAD_FOLDER,
        "folder_exists": os.path.isdir(UPLOAD_FOLDER),
    })


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "no file field in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "no file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({
        "message": "file uploaded",
        "filename": filename,
        "size_bytes": os.path.getsize(filepath),
        "saved_to": filepath,
    }), 201


@app.route("/files")
def files():
    if not os.path.isdir(UPLOAD_FOLDER):
        return jsonify({"error": "upload folder not found"}), 500

    entries = []
    for name in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, name)
        if os.path.isfile(path):
            entries.append({
                "filename": name,
                "size_bytes": os.path.getsize(path),
            })

    return jsonify({
        "upload_folder": UPLOAD_FOLDER,
        "total": len(entries),
        "files": entries,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
