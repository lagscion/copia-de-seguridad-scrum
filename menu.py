import sqlite3

conn = sqlite3.connect("reservas.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aula TEXT NOT NULL,
        fecha TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        responsable TEXT NOT NULL,
        descripcion TEXT
    )
""")

conn.commit()
conn.close()
from consultas import ConsultarReservaApp
from registroReservas import reservar_aula
import tkinter as tk
from tkinter import font

def menu():
    root = tk.Tk()
    root.title("Sistema de Reservas")
    root.geometry("420x560")
    root.resizable(False, False)
    root.configure(bg="#e8f4f8")

    #ENCABEZADO
    header = tk.Frame(root, bg="#1a7fb5", height=90)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Sistema de Reservas",
        font=("Georgia", 17, "bold"),
        bg="#1a7fb5",
        fg="white"
    ).place(relx=0.5, rely=0.5, anchor="center")

    # SUBTÍTULO
    tk.Label(
        root,
        text="Seleccione una opción",
        font=("Georgia", 11, "italic"),
        bg="#e8f4f8",
        fg="#4a7a94"
    ).pack(pady=(22, 10))

    # BOTONES
    opciones = [
        ("1.  Reservar aula",     "#1a7fb5", reservar_aula),
        ("2.  Consultar reserva", "#2196a6", lambda: consultar_reserva(root)),
        ("3.  Modificar reserva", "#2196a6", modificar_reserva),
        ("4.  Cancelar reserva",  "#e05252", cancelar_reserva),
        ("5.  Salir",             "#607d8b", lambda: salir(root)),
    ]

    for texto, color, comando in opciones:
        btn = tk.Button(
            root,
            text=texto,
            font=("Helvetica", 12),
            bg=color,
            fg="white",
            activebackground="#0d5a82",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=26,
            height=2,
            command=comando
        )
        btn.pack(pady=6)

    #INTERACCIÓN BOTÓN-CURSOR
        btn.bind("<Enter>", lambda e, b=btn, c=color: b.configure(bg=_hover(c)))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))

    #PIE DE PÁGINA
    tk.Label(
        root,
        text="© 2025 Gestión de Aulas",
        font=("Helvetica", 8),
        bg="#e8f4f8",
        fg="#90b8c8"
    ).pack(side="bottom", pady=10)

    root.mainloop()


def _hover(color):
    """Oscurece ligeramente el color al pasar el cursor."""
    mapa = {
        "#1a7fb5": "#155f8a",
        "#2196a6": "#177a88",
        "#e05252": "#b33a3a",
        "#607d8b": "#455a64",
    }
    return mapa.get(color, color)



# FUNCIONES
def consultar_reserva(ventana_principal):
    """Llama al módulo de consulta enviándole la ventana raíz."""
    ConsultarReservaApp(ventana_principal)

def modificar_reserva():
    pass

def cancelar_reserva():
    pass

def salir(root):
    print("SALIENDO...")
    root.destroy()


menu()


