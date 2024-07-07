import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class PrestamosApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)
        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_prestamo)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Agregar botón para mostrar todos los préstamos
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_prestamos)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botón para convertir a Excel
        convert_button = ttk.Button(search_frame, text="Convertir a Excel", command=self.export_to_excel)
        convert_button.pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=('idprestamo', 'idlibro', 'idusuario', 'fecha_prestamo', 'fecha_devolucion'), show='headings')
        self.tree.heading('idprestamo', text='ID')
        self.tree.heading('idlibro', text='ID Libro')
        self.tree.heading('idusuario', text='ID Usuario')
        self.tree.heading('fecha_prestamo', text='Fecha Prestamo')
        self.tree.heading('fecha_devolucion', text='Fecha Devolucion')
        self.tree.pack(expand=True, fill='both')

        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_prestamo)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.selected_item = None

    def execute_query(self, query, parameters=()):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
        connection.close()

    def populate_tree(self, search_term=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        if search_term:
            cursor.execute('SELECT * FROM prestamos WHERE idlibro LIKE ? OR idusuario LIKE ? OR fecha_prestamo LIKE ? OR fecha_devolucion LIKE ?', 
                           ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute('SELECT * FROM prestamos')
        prestamos = cursor.fetchall()
        for prestamo in prestamos:
            self.tree.insert('', tk.END, values=prestamo)
        connection.close()

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar Préstamo")

        form_frame = ttk.Frame(add_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="ID Libro:").grid(row=0, column=0)
        idlibro_entry = ttk.Entry(form_frame)
        idlibro_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="ID Usuario:").grid(row=1, column=0)
        idusuario_entry = ttk.Entry(form_frame)
        idusuario_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Fecha Préstamo (YYYY-MM-DD):").grid(row=2, column=0)
        fecha_prestamo_entry = ttk.Entry(form_frame)
        fecha_prestamo_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Fecha Devolución (YYYY-MM-DD):").grid(row=3, column=0)
        fecha_devolucion_entry = ttk.Entry(form_frame)
        fecha_devolucion_entry.grid(row=3, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.add_prestamo(
                                     idlibro_entry.get(),
                                     idusuario_entry.get(),
                                     fecha_prestamo_entry.get(),
                                     fecha_devolucion_entry.get(),
                                     add_window
                                 ))
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_prestamo(self, idlibro, idusuario, fecha_prestamo, fecha_devolucion, window):
        if idlibro and idusuario and fecha_prestamo:
            self.execute_query('''
                INSERT INTO prestamos (idlibro, idusuario, fecha_prestamo, fecha_devolucion) 
                VALUES (?, ?, ?, ?)
            ''', (idlibro, idusuario, fecha_prestamo, fecha_devolucion))
            messagebox.showinfo("Éxito", "Préstamo agregado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def search_prestamo(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_prestamos(self):
        self.search_entry.delete(0, tk.END)
        self.populate_tree()

    def show_context_menu(self, event):
        self.selected_item = self.tree.identify_row(event.y)
        if self.selected_item:
            self.tree.selection_set(self.selected_item)
            self.context_menu.post(event.x_root, event.y_root)

    def open_edit_window(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Préstamo")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="ID Libro:").grid(row=0, column=0)
        idlibro_entry = ttk.Entry(form_frame)
        idlibro_entry.insert(0, values[1])
        idlibro_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="ID Usuario:").grid(row=1, column=0)
        idusuario_entry = ttk.Entry(form_frame)
        idusuario_entry.insert(0, values[2])
        idusuario_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Fecha Préstamo (YYYY-MM-DD):").grid(row=2, column=0)
        fecha_prestamo_entry = ttk.Entry(form_frame)
        fecha_prestamo_entry.insert(0, values[3])
        fecha_prestamo_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Fecha Devolución (YYYY-MM-DD):").grid(row=3, column=0)
        fecha_devolucion_entry = ttk.Entry(form_frame)
        fecha_devolucion_entry.insert(0, values[4])
        fecha_devolucion_entry.grid(row=3, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.edit_prestamo(
                                     values[0],
                                     idlibro_entry.get(),
                                     idusuario_entry.get(),
                                     fecha_prestamo_entry.get(),
                                     fecha_devolucion_entry.get(),
                                     edit_window
                                 ))
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def edit_prestamo(self, idprestamo, idlibro, idusuario, fecha_prestamo, fecha_devolucion, window):
        if idlibro and idusuario and fecha_prestamo:
            self.execute_query('''
                UPDATE prestamos
                SET idlibro = ?, idusuario = ?, fecha_prestamo = ?, fecha_devolucion = ?
                WHERE idprestamo = ?
            ''', (idlibro, idusuario, fecha_prestamo, fecha_devolucion, idprestamo))
            messagebox.showinfo("Éxito", "Préstamo editado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def delete_prestamo(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este préstamo?")
        if confirm:
            self.execute_query('DELETE FROM prestamos WHERE idprestamo = ?', (values[0],))
            messagebox.showinfo("Éxito", "Préstamo eliminado correctamente")
            self.populate_tree()

    def export_to_excel(self):
        filename = "prestamos.xlsx"  # Nombre predeterminado del archivo
        try:
            prestamos_data = []
            for item in self.tree.get_children():
                prestamos_data.append(self.tree.item(item)['values'])

            df = pd.DataFrame(prestamos_data, columns=['ID', 'ID Libro', 'ID Usuario', 'Fecha Prestamo', 'Fecha Devolucion'])
            df.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Préstamos")
    app = PrestamosApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
