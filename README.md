# Jenkins + Docker + MySQL (Praktikum Komputasi Awan)

Aplikasi Flask yang terhubung ke database MySQL, dibangun dan di-deploy oleh pipeline Jenkins.

| Endpoint | Fungsi |
|---|---|
| GET / | Menampilkan data tabel `mahasiswa` dari MySQL |
| POST /mahasiswa | Menambah data (`{"nama": "..."}`) |
| GET /health | Cek koneksi aplikasi ke database |

Jalankan lokal: `docker compose up -d --build`, lalu buka http://localhost:5000
Pipeline: Checkout -> Build -> Build Docker Image -> Push Docker Image -> Deploy (App + Database)
