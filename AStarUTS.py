# untuk membuat GUI (tampilan program berbasis jendela)
import tkinter as tk
from tkinter import ttk, messagebox
#ntuk membuat peta interaktif (basis HTML).
import folium
# untuk membuka peta hasil folium di browser secara otomatis.
import webbrowser
# akses fungsi OS, misal untuk mengecek file.
import os
# library untuk mengakses layanan rute online (jarak, waktu tempuh).
import openrouteservice
# digunakan untuk struktur data heap (prioritas queue), biasa dipakai di algoritma pencarian rute
import heapq
# mungkin akan dipakai untuk perhitungan matematika (misal jarak Euclidean, dll).
import math
# digunakan untuk mencatat waktu atau menghitung estimasi waktu.
from datetime import datetime

# kunci API yang digunakan supaya bisa mengakses layanan dari OpenRouteService
ORS_API_KEY = "5b3ce3597851110001cf624843e7043993ae43cd8330f3d91dab22c4"

# Ini dictionary yang berisi nama lokasi (seperti "Gerbang Depan", "Gedung F", dll) yang dipetakan ke koordinat latitude dan longitude.
coordinates = {
    "Gerbang Depan": [-3.7597051, 102.2677983],
    "Pasca Hukum": [-3.7602660, 102.2686734],
    "MAKSI (Ged C)": [-3.7590706, 102.2679177],
    "Ged. B": [-3.7593362, 102.2692196],
    "Ged. A": [-3.7592326, 102.2701266],
    "Masjid Darul Ulum": [-3.7572782, 102.2675868],
    "Gedung F": [-3.7617198, 102.2686238],
    "Lab. Hukum": [-3.7605831, 102.2684417],
    "Ged. I": [-3.7603011, 102.2697707],
    "Ged. MM": [-3.7611429, 102.2699081],
    "Ged. MPP": [-3.7614596, 102.2717675],
    "Ged. J": [-3.7607740, 102.2703630],
    "Ged. UPT B. Inggris": [-3.7607740, 102.2703630],
    "Dekanat Pertanian": [-3.7593362, 102.2692196],
    "Ged. T": [-3.7580992, 102.2719195],
    "Ged. V": [-3.7571162, 102.2728366],
    "Ged. Renper": [-3.7570165, 102.2727136],
    "Lab. Agro": [-3.7566360, 102.2757012],
    "Ged. Basic Sains": [-3.7560288, 102.2747136],
    "GKB I": [-3.7568032, 102.2737209],
    "Dekanat MIPA": [-3.7560288, 102.2747136],
    "UPT Puskom": [-3.7584458, 102.2730644],
    "Rektorat": [-3.7590495, 102.2723146],
    "Gerbang Rektorat": [-3.760548, 102.272627],
    "Dekanat FISIP": [-3.7590310, 102.2741732],
    "Gerbang Belakang": [-3.7596149, 102.2752156],
    "Gerbang Keluar Belakang": [-3.759388, 102.276225],
    "Dekanat Teknik": [-3.7584642, 102.2767009],
    "Gedung Serba Guna (GSG)": [-3.7575361, 102.2765579],
    "Stadion Olahraga": [-3.7576442, 102.2781715],
    "GKB II": [-3.7578575, 102.2740375],
    "Dekanat FKIP": [-3.7575341, 102.2750444],
    "GKB III": [-3.7560850, 102.2766449],
    "Kedokteran": [-3.7551337, 102.2780320],
    "PSPD": [-3.7553463, 102.2765021],
    "PKM": [-3.7585034, 102.2750154],
    "GKB V": [-3.755526, 102.276445]
}

# Mendefinisikan Graph (Graf)
graph = {
    "Gerbang Depan": [("Pasca Hukum", {"jarak": 200, "waktu": 120})],
    "Pasca Hukum": [("Gerbang Depan", {"jarak": 200, "waktu": 120}), ("MAKSI (Ged C)", {"jarak": 300, "waktu": 180}), ("Gedung F", {"jarak": 500, "waktu": 300})],
    "MAKSI (Ged C)": [("Pasca Hukum", {"jarak": 300, "waktu": 180}), ("Ged. B", {"jarak": 200, "waktu": 120})],
    "Ged. B": [("MAKSI (Ged C)", {"jarak": 200, "waktu": 120}), ("Ged. A", {"jarak": 400, "waktu": 240})],
    "Ged. A": [("Ged. B", {"jarak": 400, "waktu": 240}), ("Masjid Darul Ulum", {"jarak": 200, "waktu": 120})],
    "Masjid Darul Ulum": [("Ged. A", {"jarak": 200, "waktu": 120})],
    "Gedung F": [("Pasca Hukum", {"jarak": 500, "waktu": 300}), ("Lab. Hukum", {"jarak": 300, "waktu": 180}), ("Ged. I", {"jarak": 400, "waktu": 240}), ("Ged. J", {"jarak": 600, "waktu": 360}), ("Dekanat Pertanian", {"jarak": 500, "waktu": 300})],
    "Lab. Hukum": [("Gedung F", {"jarak": 300, "waktu": 180})],
    "Ged. I": [("Gedung F", {"jarak": 400, "waktu": 240}), ("Ged. MM", {"jarak": 200, "waktu": 120})],
    "Ged. MM": [("Ged. I", {"jarak": 200, "waktu": 120}), ("Ged. MPP", {"jarak": 300, "waktu": 180})],
    "Ged. MPP": [("Ged. MM", {"jarak": 300, "waktu": 180}), ("Ged. UPT B. Inggris", {"jarak": 400, "waktu": 240})],
    "Ged. J": [("Gedung F", {"jarak": 600, "waktu": 360}), ("Ged. UPT B. Inggris", {"jarak": 200, "waktu": 120})],
    "Ged. UPT B. Inggris": [("Ged. J", {"jarak": 200, "waktu": 120}), ("Rektorat", {"jarak": 500, "waktu": 300})],
    "Dekanat Pertanian": [("Gedung F", {"jarak": 500, "waktu": 300}), ("Ged. T", {"jarak": 300, "waktu": 180})],
    "Ged. T": [("Dekanat Pertanian", {"jarak": 300, "waktu": 180}), ("Ged. V", {"jarak": 200, "waktu": 120})],
    "Ged. V": [("Ged. T", {"jarak": 200, "waktu": 120}), ("Ged. Renper", {"jarak": 400, "waktu": 240}), ("Rektorat", {"jarak": 500, "waktu": 300})],
    "Ged. Renper": [("Ged. V", {"jarak": 400, "waktu": 240}), ("Lab. Agro", {"jarak": 300, "waktu": 180})],
    "Lab. Agro": [("Ged. Renper", {"jarak": 300, "waktu": 180}), ("Ged. Basic Sains", {"jarak": 500, "waktu": 300})],
    "Ged. Basic Sains": [("Lab. Agro", {"jarak": 500, "waktu": 300}), ("GKB I", {"jarak": 200, "waktu": 120}), ("Dekanat MIPA", {"jarak": 400, "waktu": 240})],
    "UPT Puskom": [("Ged. V", {"jarak": 400, "waktu": 240}), ("GKB I", {"jarak": 200, "waktu": 120})],
    "Rektorat": [("Ged. UPT B. Inggris", {"jarak": 500, "waktu": 300}), ("Ged. V", {"jarak": 500, "waktu": 300}), ("Dekanat FISIP", {"jarak": 300, "waktu": 180}), ("Gerbang Rektorat", {"jarak": 50, "waktu": 200})],
    "Gerbang Rektorat": [("Rektorat", {"jarak": 50, "waktu": 200})],  # Sudah dua arah sekarang
    "Dekanat FISIP": [("Rektorat", {"jarak": 300, "waktu": 180}), ("Gerbang Belakang", {"jarak": 200, "waktu": 120}), ("GKB II", {"jarak": 300, "waktu": 180})],
    "Gerbang Belakang": [("Dekanat FISIP", {"jarak": 200, "waktu": 120}), ("Dekanat Teknik", {"jarak": 400, "waktu": 240})],
    "Gerbang Keluar Belakang": [("Dekanat Teknik", {"jarak": 100, "waktu": 200})],
    "Dekanat Teknik": [("Gerbang Belakang", {"jarak": 400, "waktu": 240}), ("Gedung Serba Guna (GSG)", {"jarak": 300, "waktu": 180}), ("Gerbang Keluar Belakang", {"jarak": 100, "waktu": 200})],
    "Gedung Serba Guna (GSG)": [("Dekanat Teknik", {"jarak": 300, "waktu": 180}), ("Stadion Olahraga", {"jarak": 400, "waktu": 240}), ("GKB III", {"jarak": 200, "waktu": 120}), ("Dekanat FKIP", {"jarak": 500, "waktu": 300})],
    "GKB I": [("UPT Puskom", {"jarak": 200, "waktu": 120}), ("GKB II", {"jarak": 300, "waktu": 180}), ("Ged. Basic Sains", {"jarak": 200, "waktu": 120})],
    "GKB II": [("GKB I", {"jarak": 300, "waktu": 180}), ("Dekanat FKIP", {"jarak": 200, "waktu": 120}), ("Dekanat FISIP", {"jarak": 300, "waktu": 180})],
    "Dekanat FKIP": [("GKB II", {"jarak": 200, "waktu": 120}), ("Gedung Serba Guna (GSG)", {"jarak": 500, "waktu": 300}), ("Dekanat FKIP", {"jarak": 350, "waktu": 180})],
    "GKB V": [("PKM", {"jarak": 300, "waktu": 180}), ("PSPD", {"jarak": 400, "waktu": 240}), ("Kedokteran", {"jarak": 250, "waktu": 120})],
    "Stadion Olahraga": [("GKB III", {"jarak": 200, "waktu": 120}), ("PSPD", {"jarak": 500, "waktu": 300})],
    "Dekanat MIPA": [("Ged. Basic Sains", {"jarak": 400, "waktu": 240})],
    "PSPD": [("Stadion Olahraga", {"jarak": 500, "waktu": 300}), ("GKB V", {"jarak": 300, "waktu": 180})],
    "GKB III": [("Gedung Serba Guna (GSG)", {"jarak": 200, "waktu": 120}), ("Stadion Olahraga", {"jarak": 400, "waktu": 240})],
    "PKM": [("GKB V", {"jarak": 300, "waktu": 180}), ("Ged. MPP", {"jarak": 400, "waktu": 240})],
    "Kedokteran": [("GKB V", {"jarak": 250, "waktu": 120}), ("Dekanat FKIP", {"jarak": 350, "waktu": 180})]
}

# Membuat dictionary 'coordinates' berisi lokasi-lokasi penting di dalam kampus
# Setiap lokasi memiliki koordinat GPS (latitude, longitude)
def get_modified_graph(): 
    now = datetime.now()  # Mendapatkan waktu saat ini
    hour = now.hour  # Mengambil jam saat ini (0-23)
    weekday = now.weekday()  # Mengambil hari dalam bentuk angka (0 = Senin, 6 = Minggu)

    # Salin struktur graf asli ke variabel baru 'modified', agar tidak mengubah graf asli
    modified = {node: list(neighbors) for node, neighbors in graph.items()}

    to_remove = set()  # Set untuk menyimpan node (simpul) yang akan dihapus

    if hour >= 16:  # Jika waktu menunjukkan pukul 16:00 ke atas (sore/malam)
        to_remove.add("Gerbang Depan"),  # Gerbang Depan ditutup
        to_remove.add("Gerbang Keluar Belakang"),  # Gerbang Keluar Belakang ditutup
        to_remove.add("Gerbang Rektorat")  # Gerbang Rektorat ditutup

    if hour <= 5:  # Jika waktu sebelum atau sama dengan pukul 05:00 pagi
        to_remove.add("Gerbang Depan"),  # Gerbang Depan ditutup
        to_remove.add("Gerbang Keluar Belakang"),  # Gerbang Keluar Belakang ditutup
        to_remove.add("Gerbang Rektorat"),  # Gerbang Rektorat ditutup
        to_remove.add("Gerbang Belakang")  # Gerbang Belakang juga ditutup

    if hour >= 22:  # Jika waktu menunjukkan pukul 22:00 ke atas (malam)
        to_remove.add("Gerbang Belakang")  # Gerbang Belakang ditutup

    if weekday >= 5:  # Jika hari Sabtu (5) atau Minggu (6)
        to_remove.add("Gerbang Depan"),  # Gerbang Depan ditutup
        to_remove.add("Gerbang Keluar Belakang"),  # Gerbang Keluar Belakang ditutup
        to_remove.add("Gerbang Rektorat")  # Gerbang Rektorat ditutup

    # Menghapus simpul yang ada di to_remove dari graf
    for node in to_remove:
        modified.pop(node, None)  # Hapus node dari dictionary jika ada

    # Untuk setiap simpul yang tersisa, hapus edge yang mengarah ke simpul yang telah dihapus
    for node in modified:
        modified[node] = [edge for edge in modified[node] if edge[0] not in to_remove]

    return modified  # Mengembalikan graf yang telah dimodifikasi

# Algoritma A* Search
def astar(graph, start, goal):
    open_list = [(0, start, [])]  # (total_cost, current_node, path)
    closed_set = set()

    while open_list:
        open_list.sort()
        cost, current, path = open_list.pop(0)

        if current == goal:
            return cost, path + [current]

        closed_set.add(current)

        for neighbor, attributes in graph.get(current, []):  # Perbaiki disini!
            if neighbor in closed_set:
                continue

            new_cost = cost + attributes['jarak']  # Kamu bisa ganti 'jarak' ke 'waktu' kalau mau pakai waktu
            open_list.append((new_cost, neighbor, path + [current]))

    return float("inf"), []

# Untuk menyimpan semua jenis kendaraan unik
def ambil_info_kendaraan(path, graph):
    kendaraan_set = set()
    for i in range(len(path) - 1):
        for neighbor, attr in graph[path[i]]:
            if neighbor == path[i + 1]:
                kendaraan_set.update(attr.get("kendaraan", []))
                break
    return kendaraan_set

# memperlihatkan map
def show_map_with_ors(path, mode_kendaraan):
    if not path:
        return None

    client = openrouteservice.Client(key=ORS_API_KEY)

    # Mapping mode ke profile ORS
    profile_map = {
        "Mobil": "driving-car",
        "Motor": "cycling-regular",
        "Jalan Kaki": "foot-walking"
    }

# Pilih profil kendaraan berdasarkan mode (motor, mobil, jalan kaki, dll)
    profile = profile_map.get(mode_kendaraan, "foot-walking")

    try:
        # Ambil koordinat start (awal) dan end (tujuan) dari path
        start = coordinates[path[0]]
        end = coordinates[path[-1]]

        # Request rute dari OpenRouteService (ORS)
        route = client.directions(
            coordinates=[start[::-1], end[::-1]], # Balik (lat, lon) -> (lon, lat) sesuai ORS
            profile=profile,    # Jenis kendaraan
            format='geojson'    # Format hasil dalam GeoJSON
        )
        
        # Ambil jalur (garis rute) dan durasi perjalanan
        geometry = route['features'][0]['geometry']['coordinates']
        duration = route['features'][0]['properties']['summary']['duration']

        # Buat peta baru di titik start
        m = folium.Map(location=start, zoom_start=17)
        folium.Marker(location=start, popup="Awal", icon=folium.Icon(color="green")).add_to(m)  # Tambahkan marker untuk titik awal
        folium.Marker(location=end, popup="Tujuan", icon=folium.Icon(color="red")).add_to(m)    # Tambahkan marker untuk titik tujuan
        folium.PolyLine(locations=[(lat, lng) for lng, lat in geometry], color="blue", weight=5).add_to(m) # Gambar garis rute di peta

        # Simpan peta ke file HTML
        m.save("jalur_terpendek.html")
        webbrowser.open("file://" + os.path.abspath("jalur_terpendek.html"))  # Buka file HTML di browser

        return duration

    except Exception as e:
        messagebox.showerror("Error saat menggambar peta", str(e)) # Kalau ada error, tampilkan messagebox error
        return None

# Fungsi untuk mencari dan menampilkan jalur terpendek
def find_path():
    # Ambil input dari combobox
    start = start_combobox.get()
    goal = goal_combobox.get()
    kendaraan = kendaraan_combobox.get()

    # Validasi input kosong
    if not start or not goal or not kendaraan:
        messagebox.showwarning("Input tidak lengkap", "Silakan pilih titik awal, tujuan, dan kendaraan.")
        return

    # Validasi start dan goal tidak boleh sama
    if start == goal:
        messagebox.showinfo("Info", "Titik awal dan tujuan tidak boleh sama.")
        return

    # Validasi koordinat tersedia di data
    if start not in coordinates or goal not in coordinates:
        messagebox.showerror("Error", "Koordinat tidak ditemukan.")
        return

    # Ambil graf yang sudah dimodifikasi sesuai kendaraan
    graph_now = get_modified_graph()

    # Cari jalur dan biaya menggunakan algoritma A*
    cost, path = astar(graph, start, goal)

    # Validasi jika jalur tidak ditemukan
    if not path:
        messagebox.showerror("Tidak ditemukan", "Tidak ada jalur dari titik awal ke tujuan.")
        return

    # Gambar rute di peta dan hitung estimasi waktu tempuh
    waktu_detik = show_map_with_ors(path, kendaraan)
    if waktu_detik is None:
        return

    # Konversi waktu dari detik ke menit
    waktu_menit = round(waktu_detik / 60)

    # Ambil info kendaraan yang tersedia di sepanjang path
    kendaraan_set = ambil_info_kendaraan(path, graph_now)
    kendaraan_text = ", ".join(sorted(kendaraan_set)) if kendaraan_set else "Tidak diketahui"

    # Susun teks hasil untuk ditampilkan
    result_text = f"Jalur tercepat dari '{start}' ke '{goal}' dengan {kendaraan}:\n\n"
    result_text += f"Estimasi waktu tempuh: {waktu_menit} menit\n"
    result_text += "Rute:\n" + " → ".join(path)

    # Tampilkan hasil ke label
    result_label.config(text=result_text)


# Fungsi untuk memperbarui isi combobox start & goal berdasarkan graph yang bisa dilalui kendaraan
def update_combobox_values():
    modified = get_modified_graph()
    filtered_places = list(modified.keys())
    start_combobox['values'] = filtered_places
    goal_combobox['values'] = filtered_places


# Fungsi untuk reset/clear hasil jika user mengganti pilihan
def reset_result(*args):
    result_label.config(text="")

import tkinter as tk
from tkinter import ttk, messagebox

# GUI
root = tk.Tk()
root.title("Pencarian Jalur Terpendek - UNIB")
root.geometry("800x650")
root.configure(bg="#eaf2f8")  # Background warna soft biru muda

# =================== JUDUL =================== #
title_label = tk.Label(
    root,
    text="Pencarian Jalur Terpendek UNIB",
    bg="#eaf2f8",
    font=("Poppins", 22, "bold"),
    fg="#2c3e50"
)
title_label.pack(pady=(25, 15))

# =================== FRAME UTAMA =================== #
main_frame = tk.Frame(root, bg="#ffffff", bd=4, relief="ridge")
main_frame.pack(padx=25, pady=10, fill="both", expand=True)

# =================== FRAME INPUT =================== #
input_frame = tk.Frame(main_frame, bg="#ffffff")
input_frame.pack(pady=20)

# Styling Label + Combobox
def create_input_row(frame, text, row, combobox_width=45, combobox_values=None):
    label = tk.Label(frame, text=text, bg="#ffffff", font=("Poppins", 13), fg="#34495e")
    label.grid(row=row, column=0, sticky="e", padx=15, pady=12)

    combobox = ttk.Combobox(frame, state="readonly", width=combobox_width)
    if combobox_values:
        combobox['values'] = combobox_values
        combobox.current(0)
    combobox.grid(row=row, column=1, padx=15, pady=12, sticky="w")
    combobox.bind("<<ComboboxSelected>>", reset_result)
    return combobox

start_combobox = create_input_row(input_frame, "Titik Awal:", 0)
goal_combobox = create_input_row(input_frame, "Tujuan:", 1)
kendaraan_combobox = create_input_row(input_frame, "Kendaraan:", 2, combobox_width=30,
                                      combobox_values=["Mobil", "Motor", "Jalan Kaki"])

# =================== FRAME BUTTON =================== #
button_frame = tk.Frame(main_frame, bg="#ffffff")  # Membuat frame baru untuk tombol dengan latar belakang putih
button_frame.pack(pady=10)  # Menempatkan frame tombol di dalam main_frame dengan padding vertikal 10px

# Gaya atau tampilan untuk tombol-tombol yang digunakan
style_button = {
    "font": ("Poppins", 11, "bold"),  # Font tombol: Poppins ukuran 11, tebal
    "width": 18,  # Lebar tombol dalam karakter
    "bd": 0,  # Border tombol diset ke 0 (tidak ada garis pinggir default)
    "relief": "ridge",  # Tampilan pinggir tombol menggunakan gaya 'ridge'
    "padx": 10,  # Padding horizontal dalam tombol
    "pady": 8  # Padding vertikal dalam tombol
}

# Tombol untuk mencari jalur (akan memanggil fungsi find_path saat diklik)
find_button = tk.Button(
    button_frame, text="🔍 Cari Jalur", command=find_path,  # Fungsi yang dipanggil saat tombol diklik
    bg="#3498db",  # Latar belakang tombol biru
    fg="white",  # Warna teks putih
    **style_button  # Gunakan gaya yang sudah didefinisikan di atas
)
find_button.grid(row=0, column=0, padx=12, pady=8)  # Menempatkan tombol di baris 0 kolom 0 dengan padding

# Tombol untuk menutup aplikasi
close_button = tk.Button(
    button_frame, text="❌ Tutup", command=root.quit,  # Menutup aplikasi saat diklik
    bg="#e74c3c",  # Latar belakang tombol merah
    fg="white",  # Warna teks putih
    **style_button  # Gunakan gaya tombol yang sama
)
close_button.grid(row=0, column=1, padx=12, pady=8)  # Menempatkan tombol di baris 0 kolom 1

# =================== FRAME HASIL =================== #
# Membuat frame untuk menampilkan hasil pencarian jalur
result_frame = tk.Frame(main_frame, bg="#ecf0f1", bd=3, relief="groove")  # Latar abu terang, border 3px
result_frame.pack(padx=25, pady=20, fill="both", expand=True)  # Ditempatkan dengan padding dan bisa meluas

# Label yang menampilkan teks hasil pencarian jalur
result_label = tk.Label(
    result_frame,
    text="Hasil pencarian jalur akan muncul di sini.",  # Teks awal/default
    bg="#ecf0f1",  # Latar label sama dengan frame
    font=("Poppins", 12),  # Font Poppins ukuran 12
    wraplength=680,  # Panjang maksimum sebelum teks terbungkus ke baris baru
    justify="left",  # Teks diratakan ke kiri
    fg="#2c3e50"  # Warna teks abu gelap
)
result_label.pack(padx=15, pady=15)  # Menempatkan label dengan padding

# =================== SETUP =================== #
update_combobox_values()  # Memperbarui nilai-nilai pada combobox (misalnya pilihan lokasi awal/tujuan)

root.mainloop()  # Menjalankan loop utama aplikasi Tkinter (menjaga jendela tetap aktif)
