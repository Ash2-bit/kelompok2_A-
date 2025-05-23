import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# ===================== Fungsi Heuristik (Sederhana) =====================
def heuristic(node, goal):
    return abs(hash(node) - hash(goal)) % 100

def calculate_cost(distance):
    return (distance // 10) * 1000

# ===================== Algoritma A* =====================
def a_star(graph, start, goal, heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))

    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal]

        for neighbor, weight in graph.get(current, []):
            tentative_g_score = g_score[current] + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None, float('inf')

# ===================== Fungsi Cari Jalur =====================
def find_path():
    start = start_combobox.get()
    goal = goal_combobox.get()

    if start == goal:
        result_label.config(text="Titik awal dan tujuan tidak boleh sama.")
        return

    if start not in graph or goal not in graph:
        messagebox.showerror("Error", "Titik tidak ditemukan di graf.")
        return

    path, cost = a_star(graph, start, goal, heuristic)
    if path:
        biaya = calculate_cost(cost)
        result = f"Jalur: {' -> '.join(path)}\nJarak: {cost} meter\nEstimasi Biaya: Rp {biaya}"
    else:
        result = "Jalur tidak ditemukan."

    result_label.config(text=result)

def reset_selection():
    start_combobox.set("")
    goal_combobox.set("")
    result_label.config(text="")

# ===================== Data Graf =====================
graph = {
    "Pintu Gerbang Depan": [("Pasca Hukum", 200)],
    "Pasca Hukum": [("Pintu Gerbang Depan", 200), ("MAKSI (Ged C)", 400), ("Gedung F", 500)],
    "MAKSI (Ged C)": [("Pasca Hukum", 400), ("Ged. B", 300)],
    "Ged. B": [("MAKSI (Ged C)", 300), ("Ged. A", 200)],
    "Ged. A": [("Ged. B", 200), ("Masjid UNIB", 100)],
    "Masjid UNIB": [("Ged. A", 100)],
    "Gedung F": [("Pasca Hukum", 500), ("Lab. Hukum", 300), ("Ged. I", 200), ("Ged. J", 200), ("Dekanat Pertanian", 200)],
    "Lab. Hukum": [("Gedung F", 100)],
    "Ged. I": [("Gedung F", 150), ("Ged. MM", 150)],
    "Ged. MM": [("Ged. I", 200), ("Ged. MPP", 200)],
    "Ged. MPP": [("Ged. MM", 100), ("Ged. UPT B. Inggris", 100)],
    "Ged. J": [("Gedung F", 100), ("Ged. UPT B. Inggris", 100)],
    "Ged. UPT B. Inggris": [("Ged. J", 100), ("REKTORAT", 150)],
    "Dekanat Pertanian": [("Gedung F", 150), ("Ged. T", 150)],
    "Ged. T": [("Dekanat Pertanian", 150), ("Ged. V", 150)],
    "Ged. V": [("Ged. T", 150), ("Ged. Renper", 150), ("REKTORAT", 150), ("UPT Puskom", 150)],
    "Ged. Renper": [("Ged. V", 150), ("Lab. Agro", 150)],
    "Lab. Agro": [("Ged. Renper", 150), ("Ged. Basic Sains", 150)],
    "Ged. Basic Sains": [("Lab. Agro", 150), ("GKB I", 150), ("Dekanat MIPA", 150)],
    "UPT Puskom": [("Ged. V", 150), ("GKB I", 150)],
    "REKTORAT": [("Ged. UPT B. Inggris", 150), ("Ged. V", 150), ("Dekanat FISIP", 150)],
    "Dekanat FISIP": [("REKTORAT", 150), ("Pintu Gerbang", 150), ("GKB II", 150)],
    "Pintu Gerbang": [("Dekanat FISIP", 150), ("Dekanat Teknik", 150)],
    "Dekanat Teknik": [("Pintu Gerbang", 150), ("Gedung Serba Guna (GSG)", 150)],
    "Gedung Serba Guna (GSG)": [("Dekanat Teknik", 150), ("Stadion Olahraga", 150), ("GKB III", 150), ("Dekanat FKIP", 150)],
    "GKB I": [("UPT Puskom", 150), ("GKB II", 150), ("Ged. Basic Sains", 150)],
    "GKB II": [("GKB I", 150), ("Dekanat FKIP", 150), ("Dekanat FISIP", 150)],
    "Dekanat FKIP": [("GKB II", 150), ("Gedung Serba Guna (GSG)", 150)],
    "GKB V": [("PKM", 150), ("PSPD", 150)],
    "Stadion Olahraga": [("GKB III", 150), ("PSPD", 150)],
    "GKB III": [("Gedung Serba Guna (GSG)", 150)],
    "PKM": [("GKB V", 150)],
    "PSPD": [("GKB V", 150), ("Stadion Olahraga", 150)],
    "Dekanat MIPA": [("Ged. Basic Sains", 150)]
}

# ===================== GUI =====================
root = tk.Tk()
root.title("A* Pathfinding - Peta Kampus UNIB")
root.geometry("700x500")
root.configure(bg="#6699CC")

tk.Label(root, text="Titik Awal").pack()
start_combobox = ttk.Combobox(root, values=list(graph.keys()), width=60)
start_combobox.pack()

tk.Label(root, text="Titik Tujuan").pack()
goal_combobox = ttk.Combobox(root, values=list(graph.keys()), width=60)
goal_combobox.pack()

tk.Button(root, text="Cari Jalur A*", command=find_path, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="Reset", command=reset_selection, bg="red", fg="white").pack(pady=5)

result_label = tk.Label(root, text="", justify="left", wraplength=650, anchor="w")
result_label.pack(pady=20, fill=tk.BOTH, expand=True)

root.mainloop()
