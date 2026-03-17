import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ConsultarReservaApp:
    def __init__(self, root_parent):
        self.root = tk.Toplevel(root_parent)
        self.root.geometry("600x500")
        self.root.configure(bg="#1e1e26")  # Fondo oscuro profesional

        # Configuración de estilos personalizados
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilo para el contenedor de datos
        self.style.configure("Card.TFrame", background="#2d2d3a", relief="flat")
        self.style.configure("Header.TLabel", 
                             background="#1e1e26", 
                             foreground="#ffffff", 
                             font=("Segoe UI", 16, "bold"))
        
        self.style.configure("Data.TLabel", 
                             background="#2d2d3a", 
                             foreground="#dcdcdc", 
                             font=("Segoe UI", 10))
                             
        self.style.configure("Value.TLabel", 
                             background="#2d2d3a", 
                             foreground="#4cc9f0", 
                             font=("Segoe UI", 10, "bold"))

        self.crear_interfaz()

# ... (todo el código anterior de la clase se mantiene igual hasta el final de crear_interfaz)

    def crear_interfaz(self):
        # Título principal
        header = ttk.Label(self.root, text="SISTEMA DE GESTIÓN DE AULAS", style="Header.TLabel")
        header.pack(pady=(25, 10))

        # Marco de búsqueda (Entry + Botón Buscar)
        search_frame = tk.Frame(self.root, bg="#1e1e26")
        search_frame.pack(pady=10)

        self.entry_id = tk.Entry(search_frame, width=15, font=("Segoe UI", 12), bg="#3b3b4d", 
                                 fg="white", insertbackground="white", border=0)
        self.entry_id.pack(side="left", padx=10, ipady=5)

        btn_buscar = tk.Button(search_frame, text="BUSCAR ID", command=self.buscar_reserva,
                               bg="#4cc9f0", fg="#1e1e26", font=("Segoe UI", 9, "bold"),
                               relief="flat", padx=20, cursor="hand2")
        btn_buscar.pack(side="left")

        # Contenedor de información (Estilo Card)
        self.card = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        self.card.pack(padx=40, pady=20, fill="both", expand=True)

        self.detalles = {}
        campos = [
            ("Aula", "aula"), ("Fecha", "fecha"), ("Hora Inicio", "hora_inicio"),
            ("Hora Fin", "hora_fin"), ("Responsable", "responsable"), ("Descripción", "descripcion")
        ]
        
        for i, (label_text, key) in enumerate(campos):
            row_frame = tk.Frame(self.card, bg="#2d2d3a")
            row_frame.pack(fill="x", pady=8)
            ttk.Label(row_frame, text=f"{label_text.upper()}:", style="Data.TLabel", width=15).pack(side="left")
            val = ttk.Label(row_frame, text="---", style="Value.TLabel")
            val.pack(side="left")
            self.detalles[key] = val

        # --- AQUÍ ESTÁ EL NUEVO BOTÓN PARA VOLVER ---
        btn_volver = tk.Button(self.root, 
                               text="VOLVER AL MENÚ", 
                               command=self.root.destroy, # Cierra solo esta ventana
                               bg="#e05252", # Rojo para diferenciarlo de la búsqueda
                               fg="white",
                               font=("Segoe UI", 9, "bold"),
                               relief="flat",
                               pady=10,
                               cursor="hand2")
        btn_volver.pack(fill="x", padx=40, pady=(0, 20))

# ... (el resto de las funciones buscar_reserva y limpiar_datos siguen igual)

    def buscar_reserva(self):
        reserva_id = self.entry_id.get()
        
        if not reserva_id.isdigit():
            messagebox.showwarning("Atención", "Ingrese un ID válido.")
            return

        try:
            # Conexión a la base de datos compartida reservas.db [cite: 38, 119]
            conn = sqlite3.connect('reservas.db')
            cursor = conn.cursor()
            
            # Selección de columnas específicas del esquema 
            cursor.execute("""
                SELECT aula, fecha, hora_inicio, hora_fin, responsable, descripcion 
                FROM reservas WHERE id = ?
            """, (reserva_id,))
            
            row = cursor.fetchone()
            conn.close()

            if row:
                data = {
                    "aula": row[0],
                    "fecha": row[1],
                    "hora_inicio": row[2],
                    "hora_fin": row[3],
                    "responsable": row[4],
                    "descripcion": row[5]
                }
                for key, value in data.items():
                    self.detalles[key].config(text=str(value))
            else:
                self.limpiar_datos()
                messagebox.showinfo("Búsqueda", f"No se encontró la reserva con ID: {reserva_id}")

        except sqlite3.Error as e:
            messagebox.showerror("Error de Sistema", f"Error en la base de datos: {e}")

    def limpiar_datos(self):
        for lbl in self.detalles.values():
            lbl.config(text="---")

