import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class EliminarReservaApp:
    def __init__(self, root_parent):
        self.root = tk.Toplevel(root_parent)
        self.root.title("Eliminar Reservación")
        self.root.geometry("500x300")
        self.root.configure(bg="#1e1e26") # Fondo oscuro profesional [consultas.py]

        # Configuración de estilos (Heredados de tu estética actual)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        tk.Label(self.root, text="ELIMINAR RESERVACIÓN", bg="#1e1e26", fg="white", 
                 font=("Segoe UI", 14, "bold")).pack(pady=20)

        # Contenedor de entrada
        frame_input = tk.Frame(self.root, bg="#1e1e26")
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="ID DE RESERVA:", bg="#1e1e26", fg="#dcdcdc", 
                 font=("Segoe UI", 10)).pack(side="left", padx=5)
        
        self.entry_id = tk.Entry(frame_input, width=10, font=("Segoe UI", 12), bg="#3b3b4d", 
                                 fg="white", insertbackground="white", border=0)
        self.entry_id.pack(side="left", padx=5, ipady=3)

        # Botón de acción principal
        btn_eliminar = tk.Button(self.root, text="CONFIRMAR ELIMINACIÓN", 
                                 command=self.confirmar_eliminacion,
                                 bg="#e05252", fg="white", font=("Segoe UI", 9, "bold"),
                                 relief="flat", padx=20, pady=10, cursor="hand2")
        btn_eliminar.pack(pady=20)

        # Botón para cerrar
        btn_cancelar = tk.Button(self.root, text="CANCELAR", command=self.root.destroy,
                                 bg="#2d2d3a", fg="white", font=("Segoe UI", 9),
                                 relief="flat", padx=10, cursor="hand2")
        btn_cancelar.pack()

    def confirmar_eliminacion(self):
        reserva_id = self.entry_id.get()
        
        if not reserva_id.isdigit():
            messagebox.showwarning("Atención", "Por favor, ingrese un ID numérico válido.", parent=self.root)
            return

        try:
            # 1. Buscar la información antes de preguntar 
            conn = sqlite3.connect('reservas.db')
            cursor = conn.cursor()
            cursor.execute("SELECT aula, fecha, hora_inicio FROM reservas WHERE id = ?", (reserva_id,))
            reserva = cursor.fetchone()
            conn.close()

            if reserva:
                # 2. Construir el mensaje con los detalles de la reserva 
                aula, fecha, hora = reserva
                mensaje = (
                    f"¿Estás seguro de eliminar la siguiente reserva?\n\n"
                    f"ID: {reserva_id}\n"
                    f"AULA: {aula}\n"
                    f"FECHA: {fecha}\n"
                    f"HORA: {hora}\n\n"
                    "Esta acción no se puede deshacer."
                )
                
                # 3. Pedir confirmación final
                confirmar = messagebox.askyesno("Confirmar Eliminación", mensaje, parent=self.root)
                
                if confirmar:
                    self.ejecutar_sql(reserva_id)
            else:
                messagebox.showinfo("Búsqueda", f"No se encontró ninguna reserva con el ID: {reserva_id}",parent=self.root)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al consultar la base de datos: {e}",parent=self.root)
    def ejecutar_sql(self, reserva_id):
        try:
            # Conexión a la base de datos reservas.db 
            conn = sqlite3.connect('reservas.db')
            cursor = conn.cursor()
            
            # Ejecución del borrado
            cursor.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Éxito", f"Reserva con ID {reserva_id} eliminada.",parent=self.root)
                self.entry_id.delete(0, tk.END)
            else:
                messagebox.showinfo("Búsqueda", "No existe ninguna reserva con ese ID.",parent=self.root)
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la base de datos: {e}",parent=self.root)