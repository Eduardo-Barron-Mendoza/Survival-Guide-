import tkinter as tk
from tkinter import ttk
from contenido import REGLAS

BG     = "#f0f4f8"
PANEL  = "#ffffff"
ACENTO = "#1a73e8"
TEXTO  = "#1c1c2e"
GRIS   = "#8a9bb0"
FUENTE   = ("Consolas", 11)
FUENTE_T = ("Consolas", 12, "bold")
FUENTE_G = ("Consolas", 18, "bold")

nombres = [
    "La Camara de las Reglas",
    "El Oraculo de las Notas",
    "Skills a Desbloquear",
    "La Linea del Tiempo",
]

root = tk.Tk()
root.title("Survival Guide")
root.configure(bg=BG)
root.geometry("920x640")
root.resizable(False, False)


def limpiar(frame):
    for w in frame.winfo_children():
        w.destroy()


def mostrar_reglas():
    limpiar(area)

    tk.Label(area, text="La Camara de las Reglas", font=FUENTE_G,
             bg=PANEL, fg=ACENTO).pack(anchor="w", padx=24, pady=(20, 14))

    canvas = tk.Canvas(area, bg=PANEL, highlightthickness=0)
    scroll = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    interior = tk.Frame(canvas, bg=PANEL)
    canvas.create_window((0, 0), window=interior, anchor="nw")
    interior.bind("<Configure>",
                  lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    for i, regla in enumerate(REGLAS, 1):
        fila = tk.Frame(interior, bg=PANEL)
        fila.pack(fill="x", padx=24, pady=4)

        tk.Label(fila, text=f"{i}.", font=FUENTE_T, bg=PANEL,
                 fg=ACENTO, anchor="nw", width=3).pack(side="left", anchor="n")

        tk.Label(fila, text=regla, font=FUENTE, bg=PANEL, fg=TEXTO,
                 wraplength=520, justify="left", anchor="nw").pack(side="left", anchor="n")


def navegar(indice):
    if indice == 0:
        mostrar_reglas()


# ── sidebar 
sidebar = tk.Frame(root, bg=PANEL, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="SURVIVAL GUIDE", font=("Consolas", 13, "bold"),
         bg=PANEL, fg=ACENTO).pack(pady=(24, 2))
tk.Label(sidebar, text="El Reto Movil", font=("Consolas", 9),
         bg=PANEL, fg=GRIS).pack(pady=(0, 20))

tk.Frame(sidebar, bg="#dce3ed", height=1).pack(fill="x", padx=18, pady=4)

for i, nombre in enumerate(nombres):
    tk.Button(sidebar, text=nombre, font=("Consolas", 10), bg=PANEL,
              relief="flat", anchor="w", padx=14, pady=9,
              fg=ACENTO if i == 0 else GRIS,
              cursor="hand2" if i == 0 else "arrow",
              command=lambda idx=i: navegar(idx)).pack(fill="x", padx=6, pady=1)

# ── area de contenido 
area = tk.Frame(root, bg=PANEL)
area.pack(side="right", fill="both", expand=True)

tk.Label(area, text="Bienvenido, estudiante.", font=FUENTE_G,
         bg=PANEL, fg=ACENTO).pack(expand=True)
tk.Label(area, text="Selecciona un nivel para comenzar.",
         font=FUENTE, bg=PANEL, fg=GRIS).pack()

root.mainloop()