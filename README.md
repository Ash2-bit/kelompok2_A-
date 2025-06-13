# kelompok2_A-
kelompok2

### 🔹 Bagian Import Library
```python
import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser
import os
import openrouteservice
import heapq
import math
from datetime import datetime
```

**Analisis:**
- `tkinter`, `ttk`, `messagebox`: Untuk membuat GUI aplikasi (misalnya dropdown, tombol, dialog peringatan).
- `folium`: Untuk membuat peta interaktif berbasis HTML.
- `webbrowser`: Untuk membuka peta di browser secara otomatis.
- `os`: Untuk operasi sistem (misal pengecekan file).
- `openrouteservice`: Untuk mendapatkan rute/arah dari layanan OpenRouteService (dengan API).
- `heapq`: Untuk struktur data heap (prioritas antrian), biasa digunakan di algoritma pencarian.
- `math`: Untuk operasi matematika, misalnya jarak Euclidean (meskipun belum dipakai dalam kode ini).
- `datetime`: Untuk mengecek waktu saat ini, digunakan dalam logika buka-tutup gerbang.

---

### 🔹 Konstanta API Key
```python
ORS_API_KEY = "..."
```

**Analisis:** Ini adalah kunci API publik dari OpenRouteService yang memungkinkan aplikasi menggunakan layanan mereka seperti penentuan rute tercepat.

---

### 🔹 Dictionary Koordinat Lokasi Kampus
```python
coordinates = {
  "Gerbang Depan": [-3.7597051, 102.2677983],
  ...
}
```

**Analisis:** Menyimpan **nama tempat** (misalnya "Gedung A") dan **koordinat GPS-nya** (latitude, longitude). Ini berguna untuk:
- Menampilkan lokasi pada peta (`folium`).
- Menghubungkan titik pada graf dan peta.

---

### 🔹 Struktur Graph Kampus
```python
graph = {
  "Gerbang Depan": [("Pasca Hukum", {"jarak": 200, "waktu": 120})],
  ...
}
```

**Analisis:**
- Ini adalah representasi graf **berarah dan berbobot** (dengan bobot "jarak" dan "waktu").
- Setiap node (lokasi) menyimpan daftar tetangga dan nilai bobot antar titik.

---

### 🔹 Fungsi Modifikasi Graf Berdasarkan Waktu
```python
def get_modified_graph():
    ...
```

**Analisis:**
- Mengecek **jam sekarang** dan **hari sekarang**.
- Menutup simpul tertentu (seperti "Gerbang Depan", "Gerbang Belakang") jika sudah sore, malam, atau akhir pekan.
- Menghapus simpul dari graf dan menghapus semua edge yang terhubung ke simpul yang dihapus.
- Tujuannya agar pencarian rute tidak bisa melewati simpul-simpul yang sudah "ditutup".

📌 *Contoh kondisi real:*
- Pukul 17:00 → "Gerbang Depan" tertutup.
- Hari Minggu → Semua gerbang utama tertutup.

---

### 🔹 Algoritma Pencarian Jalur: A*
```python
def astar(graph, start, goal):
    ...
```

**Analisis:**
- Versi sederhana dari **A* Search** tanpa heuristik (sama seperti Dijkstra).
- `open_list` menyimpan node yang akan diperiksa (dengan cost total).
- `closed_set` mencegah memeriksa node yang sudah dikunjungi.
- Untuk setiap node tetangga, biaya (`cost`) dihitung berdasarkan `jarak`.

### 🔹 Fungsi Mengambil Jenis Kendaraan dari Jalur
```python
def ambil_info_kendaraan(path, graph):
    ...
```

**Analisis:**
- Mengecek rute yang telah ditemukan (`path`), lalu melihat atribut `kendaraan` (jika ada) dari edge antar titik.
- **Tujuannya mungkin untuk memfilter atau menampilkan kendaraan yang bisa melewati jalur tersebut.**

Namun, **data `kendaraan` belum tampak** di `graph`, jadi fungsi ini masih *standby*.

---

### 🔹 Fungsi Peta: `show_map_with_ors()`
```python
def show_map_with_ors(path, mode_kendaraan):
    if not path:
        return...
```

**Analisis:**
- Akan menampilkan jalur yang ditemukan dalam bentuk peta (pakai `folium`).
- `mode_kendaraan` digunakan untuk memilih mode rute dari OpenRouteService (jalan kaki, mobil, sepeda, dll).
- Biasanya akan:
  - Menambahkan marker untuk lokasi awal & akhir.
  - Menampilkan garis lintasan.
  - Membuka hasil di browser.

---


### Anggota kelompok

1. Refki Andreas Pratama
2. Habib Eddler Marpen
3. Rahman Firdaus Ilaihi
4. Abim Bintang Audio
5. Ajis Saputra Hidayah 



