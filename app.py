import os

import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppass123"),
        database=os.getenv("DB_NAME", "praktikum"),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


@app.route("/")
def index():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, nama, dibuat FROM mahasiswa ORDER BY id")
        rows = cur.fetchall()
    return jsonify(pesan="Halo dari Flask + MySQL + Docker + Jenkins!", data=rows)


@app.route("/mahasiswa", methods=["POST"])
def tambah():
    nama = (request.get_json(silent=True) or {}).get("nama", "").strip()
    if not nama:
        return jsonify(error="field 'nama' wajib diisi"), 400
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO mahasiswa (nama) VALUES (%s)", (nama,))
        conn.commit()
    return jsonify(pesan="berhasil ditambahkan", nama=nama), 201


@app.route("/health")
def health():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
        return jsonify(status="ok", database="terhubung")
    except Exception as exc:  # noqa: BLE001
        return jsonify(status="error", detail=str(exc)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
