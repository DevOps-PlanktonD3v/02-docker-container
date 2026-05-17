import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Konfigurasi dari environment variable
PORT          = int(os.environ.get("PORT", 5000))
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "/shared/uploads")

# Buat folder upload saat aplikasi start
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ── Routes ────────────────────────────────────────────────

# GET / — info aplikasi
@app.route("/")
def index():
    return jsonify({
        "app":           "Flask Shared Storage App",
        "instance":      os.environ.get("INSTANCE_NAME", "unknown"),
        "upload_folder": UPLOAD_FOLDER,
        "endpoints": {
            "GET  /":       "Halaman ini",
            "POST /upload": "Upload file (form-data, key: 'file')",
            "GET  /files":  "Daftar semua file di shared storage",
        }
    })


# POST /upload — simpan file ke shared storage
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file. Gunakan form-data dengan key 'file'"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nama file kosong"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    return jsonify({
        "message":    "File berhasil diupload ke shared storage",
        "filename":   file.filename,
        "saved_to":   save_path,
        "size_bytes": os.path.getsize(save_path),
        "uploaded_by": os.environ.get("INSTANCE_NAME", "unknown"),
    }), 201


# GET /files — tampilkan semua file di shared storage
@app.route("/files")
def list_files():
    try:
        entries = os.listdir(UPLOAD_FOLDER)
    except FileNotFoundError:
        return jsonify({"error": f"Folder '{UPLOAD_FOLDER}' tidak ditemukan"}), 500

    files = []
    for name in sorted(entries):
        full_path = os.path.join(UPLOAD_FOLDER, name)
        if os.path.isfile(full_path):
            files.append({
                "filename":   name,
                "size_bytes": os.path.getsize(full_path),
                "path":       full_path,
            })

    return jsonify({
        "upload_folder": UPLOAD_FOLDER,
        "read_by":       os.environ.get("INSTANCE_NAME", "unknown"),
        "total":         len(files),
        "files":         files,
    })


# ── Entry point ───────────────────────────────────────────

if __name__ == "__main__":
    instance = os.environ.get("INSTANCE_NAME", "unknown")
    print(f"[{instance}] Server berjalan di http://0.0.0.0:{PORT}")
    print(f"[{instance}] Shared folder : {UPLOAD_FOLDER}")
    app.run(host="0.0.0.0", port=PORT)
