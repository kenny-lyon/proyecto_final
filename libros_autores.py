import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class LibrosAutoresApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)
        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_libro_autor)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Agregar botón para mostrar todos los registros
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_libros_autores)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botón para convertir a Excel
        convert_button = ttk.Button(search_frame, text="Convertir a Excel", command=self.export_to_excel)
        convert_button.pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=('idlibro', 'idautor'), show='headings')
        self.tree.heading('idlibro', text='ID Libro')
        self.tree.heading('idautor', text='ID Autor')
        self.tree.pack(expand=True, fill='both')

        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_libro_autor)

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
            cursor.execute('SELECT * FROM libros_autores WHERE idlibro LIKE ? OR idautor LIKE ?', 
                           ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute('SELECT * FROM libros_autores')
        libros_autores = cursor.fetchall()
        for libro_autor in libros_autores:
            self.tree.insert('', tk.END, values=libro_autor)
        connection.close()

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar Libro-Autor")

        form_frame = ttk.Frame(add_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="ID Libro:").grid(row=0, column=0)
        idlibro_entry = ttk.Entry(form_frame)
        idlibro_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="ID Autor:").grid(row=1, column=0)
        idautor_entry = ttk.Entry(form_frame)
        idautor_entry.grid(row=1, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.add_libro_autor(
                                     idlibro_entry.get(),
                                     idautor_entry.get(),
                                     add_window
                                 ))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_libro_autor(self, idlibro, idautor, window):
        if idlibro and idautor:
            self.execute_query('''
                INSERT INTO libros_autores (idlibro, idautor) 
                VALUES (?, ?)
            ''', (idlibro, idautor))
            messagebox.showinfo("Éxito", "Libro-autor agregado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def search_libro_autor(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_libros_autores(self):
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
        edit_window.title("Editar Libro-Autor")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="ID Libro:").grid(row=0, column=0)
        idlibro_entry = ttk.Entry(form_frame)
        idlibro_entry.insert(0, values[0])
        idlibro_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="ID Autor:").grid(row=1, column=0)
        idautor_entry = ttk.Entry(form_frame)
        idautor_entry.insert(0, values[1])
        idautor_entry.grid(row=1, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.edit_libro_autor(
                                     values[0],
                                     idlibro_entry.get(),
                                     idautor_entry.get(),
                                     edit_window
                                 ))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def edit_libro_autor(self, old_idlibro, idlibro, idautor, window):
        if idlibro and idautor:
            self.execute_query('''
                UPDATE libros_autores
                SET idlibro = ?, idautor = ?
                WHERE idlibro = ? AND idautor = ?
            ''', (idlibro, idautor, old_idlibro, idautor))
            messagebox.showinfo("Éxito", "Libro-Autor editado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def delete_libro_autor(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta relación libro-autor?")
        if confirm:
            self.execute_query('DELETE FROM libros_autores WHERE idlibro = ? AND idautor = ?', (values[0], values[1]))
            messagebox.showinfo("Éxito", "Libro-Autor eliminado correctamente")
            self.populate_tree()

    def export_to_excel(self):
        filename = "libros_autores.xlsx"  # Nombre predeterminado del archivo
        try:
            libros_autores_data = []
            for item in self.tree.get_children():
                libros_autores_data.append(self.tree.item(item)['values'])

            df = pd.DataFrame(libros_autores_data, columns=['ID Libro', 'ID Autor'])
            df.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a '{filename}' correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Libros-Autores")
    app = LibrosAutoresApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
