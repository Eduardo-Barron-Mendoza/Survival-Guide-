import tkinter as tk
from tkinter import ttk, messagebox
from contenido import REGLAS, EVALUACION, OBJETIVOS, FECHAS
from preguntas import get_preguntas

BG     = "#f0f4f8"
PANEL  = "#ffffff"
ACENTO = "#1a73e8"
TEXTO  = "#1c1c2e"
GRIS   = "#8a9bb0"
VERDE  = "#16a34a"
FUENTE   = ("Consolas", 11)
FUENTE_T = ("Consolas", 12, "bold")
FUENTE_G = ("Consolas", 18, "bold")

nombres = [
    "La Camara de las Reglas",
    "El Oraculo de las Notas",
    "Skills a Desbloquear",
    "La Linea del Tiempo",
]
secciones     = ["reglas", "evaluacion", "objetivos", "fechas"]
desbloqueadas = [True, False, False, False]
botones_nav   = []

root = tk.Tk()
root.title("Survival Guide")
root.configure(bg=BG)
root.geometry("920x640")
root.resizable(False, False)


def limpiar(frame):
    for w in frame.winfo_children():
        w.destroy()


def actualizar_nav():
    for i, btn in enumerate(botones_nav):
        btn.config(fg=ACENTO if desbloqueadas[i] else GRIS,
                   cursor="hand2" if desbloqueadas[i] else "arrow")


# ── checkbox de compromiso ────────────────────────────────────────────────────
def mostrar_checkbox(indice):
    limpiar(area)
    tk.Label(area, text="Bien hecho!", font=FUENTE_G,
             bg=PANEL, fg=VERDE).pack(pady=(60, 10))
    tk.Label(area, text="Respondiste correctamente. Acepta el compromiso para continuar.",
             font=FUENTE, bg=PANEL, fg=GRIS, wraplength=500).pack(pady=(0, 30))

    var = tk.BooleanVar()

    def al_marcar():
        if var.get() and indice + 1 < len(desbloqueadas):
            desbloqueadas[indice + 1] = True
            actualizar_nav()
            limpiar(area)
            tk.Label(area, text="Seccion completada.", font=FUENTE_G,
                     bg=PANEL, fg=VERDE).pack(expand=True)
            tk.Label(area, text="Puedes avanzar al siguiente nivel.",
                     font=FUENTE, bg=PANEL, fg=GRIS).pack()

    tk.Checkbutton(area,
                   text="Me comprometo a cumplir con lo aprendido en esta seccion.",
                   variable=var, command=al_marcar,
                   font=FUENTE, bg=PANEL, fg=TEXTO,
                   selectcolor=PANEL, activebackground=PANEL).pack()


# ── quiz ──────────────────────────────────────────────────────────────────────
def mostrar_quiz(indice):
    limpiar(area)
    preguntas  = get_preguntas(secciones[indice], 2)
    vars_resp  = []

    tk.Label(area, text="Quiz", font=FUENTE_G,
             bg=PANEL, fg=ACENTO).pack(anchor="w", padx=24, pady=(20, 4))
    tk.Label(area, text="Responde las 2 preguntas correctamente para continuar.",
             font=FUENTE, bg=PANEL, fg=GRIS).pack(anchor="w", padx=24, pady=(0, 16))

    for i, p in enumerate(preguntas):
        tk.Label(area, text=f"{i+1}.  {p['pregunta']}", font=FUENTE_T,
                 bg=PANEL, fg=TEXTO, wraplength=580, justify="left").pack(
                 anchor="w", padx=24, pady=(8, 4))

        var = tk.StringVar(value="")
        vars_resp.append((var, p["respuesta"]))
        opciones = ["Verdadero", "Falso"] if p["tipo"] == "verdadero_falso" else p["opciones"]

        for op in opciones:
            tk.Radiobutton(area, text=op, variable=var, value=op,
                           font=FUENTE, bg=PANEL, fg=TEXTO,
                           selectcolor=PANEL, activebackground=PANEL,
                           activeforeground=ACENTO).pack(anchor="w", padx=48)

    def verificar():
        correctas = sum(1 for v, r in vars_resp if v.get() == r)
        if correctas == 2:
            mostrar_checkbox(indice)
        else:
            messagebox.showwarning("Reintentar",
                f"Tuviste {correctas} de 2 correctas. Se cambiaran las preguntas.")
            mostrar_quiz(indice)

    tk.Button(area, text="Verificar", font=FUENTE_T,
              bg=ACENTO, fg="white", relief="flat",
              cursor="hand2", command=verificar).pack(pady=24)


# ── seccion reglas ────────────────────────────────────────────────────────────
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

    tk.Button(interior, text="Ir al quiz", font=FUENTE_T,
              bg=ACENTO, fg="white", relief="flat", cursor="hand2",
              command=lambda: mostrar_quiz(0)).pack(pady=20)


# ── seccion evaluacion ────────────────────────────────────────────────────────
def mostrar_evaluacion():
    limpiar(area)
    tk.Label(area, text="El Oraculo de las Notas", font=FUENTE_G,
             bg=PANEL, fg=ACENTO).pack(anchor="w", padx=24, pady=(20, 14))

    criterios = EVALUACION["criterios"]
    parciales = EVALUACION["parciales"]

    frame_tabla = tk.Frame(area, bg=PANEL)
    frame_tabla.pack(padx=24, pady=4, anchor="w")

    # encabezados
    tk.Label(frame_tabla, text="Criterio", font=FUENTE_T, bg=PANEL,
             fg=TEXTO, width=28, anchor="w").grid(row=0, column=0, padx=4, pady=4)
    for j, parcial in enumerate(parciales.keys()):
        tk.Label(frame_tabla, text=parcial, font=FUENTE_T, bg=PANEL,
                 fg=ACENTO, width=6).grid(row=0, column=j+1, padx=4, pady=4)

    tk.Frame(frame_tabla, bg=GRIS, height=1).grid(
        row=1, column=0, columnspan=4, sticky="ew", pady=2)

    # filas
    for i, criterio in enumerate(criterios):
        tk.Label(frame_tabla, text=criterio, font=FUENTE, bg=PANEL,
                 fg=TEXTO, width=28, anchor="w").grid(row=i+2, column=0, padx=4, pady=6)
        for j, valores in enumerate(parciales.values()):
            tk.Label(frame_tabla, text=f"{valores[i]}%", font=FUENTE,
                     bg=PANEL, fg=TEXTO, width=6).grid(row=i+2, column=j+1, padx=4, pady=6)

    tk.Button(area, text="Ir al quiz", font=FUENTE_T,
              bg=ACENTO, fg="white", relief="flat", cursor="hand2",
              command=lambda: mostrar_quiz(1)).pack(pady=24)

# Objetivos
def mostrar_objetivos():
    limpiar(area)
    tk.Label(area, text="Skills a Desbloquear", font=FUENTE_G,
             bg=PANEL, fg=ACENTO).pack(anchor="w", padx=24, pady=(20, 14))

    tk.Label(area, text="Objetivo general", font=FUENTE_T,
             bg=PANEL, fg=TEXTO).pack(anchor="w", padx=24, pady=(0, 4))
    tk.Label(area, text=OBJETIVOS["general"], font=FUENTE,
             bg=PANEL, fg=TEXTO, wraplength=580,
             justify="left").pack(anchor="w", padx=24, pady=(0, 16))

    tk.Label(area, text="Competencias", font=FUENTE_T,
             bg=PANEL, fg=TEXTO).pack(anchor="w", padx=24, pady=(0, 4))
    tk.Label(area, text=OBJETIVOS["competencias"], font=FUENTE,
             bg=PANEL, fg=TEXTO, wraplength=580,
             justify="left").pack(anchor="w", padx=24, pady=(0, 24))

    tk.Button(area, text="Ir al quiz", font=FUENTE_T,
              bg=ACENTO, fg="white", relief="flat", cursor="hand2",
              command=lambda: mostrar_quiz(2)).pack(anchor="w", padx=24)

# ── navegacion ────────────────────────────────────────────────────────────────
def navegar(indice):
    if not desbloqueadas[indice]:
        messagebox.showinfo("Bloqueado",
            "Completa el nivel anterior para desbloquear este.")
        return
    if indice == 0:
        mostrar_reglas()
    elif indice == 1:
        mostrar_evaluacion()
    elif indice == 2:
        mostrar_objetivos()


# ── sidebar ───────────────────────────────────────────────────────────────────
sidebar = tk.Frame(root, bg=PANEL, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="SURVIVAL GUIDE", font=("Consolas", 13, "bold"),
         bg=PANEL, fg=ACENTO).pack(pady=(24, 2))
tk.Label(sidebar, text="El Reto Movil", font=("Consolas", 9),
         bg=PANEL, fg=GRIS).pack(pady=(0, 20))

tk.Frame(sidebar, bg="#dce3ed", height=1).pack(fill="x", padx=18, pady=4)

for i, nombre in enumerate(nombres):
    btn = tk.Button(sidebar, text=nombre, font=("Consolas", 10), bg=PANEL,
                    relief="flat", anchor="w", padx=14, pady=9,
                    fg=ACENTO if desbloqueadas[i] else GRIS,
                    cursor="hand2" if desbloqueadas[i] else "arrow",
                    command=lambda idx=i: navegar(idx))
    btn.pack(fill="x", padx=6, pady=1)
    botones_nav.append(btn)

# ── area de contenido ─────────────────────────────────────────────────────────
area = tk.Frame(root, bg=PANEL)
area.pack(side="right", fill="both", expand=True)

tk.Label(area, text="Bienvenido, estudiante.", font=FUENTE_G,
         bg=PANEL, fg=ACENTO).pack(expand=True)
tk.Label(area, text="Selecciona un nivel para comenzar.",
         font=FUENTE, bg=PANEL, fg=GRIS).pack()

root.mainloop()