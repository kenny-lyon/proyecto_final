import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class CategoriasApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)

        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_categoria)
        search_button.pack(side=tk.LEFT, padx=5)

        # Botón para mostrar todos los registros
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_categorias)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botón para convertir a Excel
        convert_button = ttk.Button(search_frame, text="Convertir a Excel", command=self.convert_to_excel)
        convert_button.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self, columns=('idcategoria', 'NOMBRE_CATEGORIA', 'UBICACION'), show='headings')
        self.tree.heading('idcategoria', text='ID')
        self.tree.heading('NOMBRE_CATEGORIA', text='Nombre Categoría')
        self.tree.heading('UBICACION', text='Ubicación')
        self.tree.pack(expand=True, fill='both')

        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_categoria)

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
            cursor.execute('''
                SELECT * FROM categorias 
                WHERE NOMBRE_CATEGORIA LIKE ? OR UBICACION LIKE ?
            ''', ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute('SELECT * FROM categorias')
        categorias = cursor.fetchall()
        for categoria in categorias:
            self.tree.insert('', tk.END, values=categoria)
        connection.close()

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar Categoría")

        form_frame = ttk.Frame(add_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="Nombre Categoría:").grid(row=0, column=0)
        nombre_categoria_entry = ttk.Entry(form_frame)
        nombre_categoria_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Ubicación:").grid(row=1, column=0)
        ubicacion_entry = ttk.Entry(form_frame)
        ubicacion_entry.grid(row=1, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.add_categoria(
                                     nombre_categoria_entry.get(),
                                     ubicacion_entry.get(),
                                     add_window
                                 ))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_categoria(self, nombre_categoria, ubicacion, window):
        if nombre_categoria and ubicacion:
            self.execute_query('''
                INSERT INTO categorias (NOMBRE_CATEGORIA, UBICACION) 
                VALUES (?, ?)
            ''', (nombre_categoria, ubicacion))
            messagebox.showinfo("Éxito", "Categoría agregada correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def search_categoria(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_categorias(self):
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
        edit_window.title("Editar Categoría")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="Nombre Categoría:").grid(row=0, column=0)
        nombre_categoria_entry = ttk.Entry(form_frame)
        nombre_categoria_entry.insert(0, values[1])
        nombre_categoria_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Ubicación:").grid(row=1, column=0)
        ubicacion_entry = ttk.Entry(form_frame)
        ubicacion_entry.insert(0, values[2])
        ubicacion_entry.grid(row=1, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.edit_categoria(
                                     values[0],
                                     nombre_categoria_entry.get(),
                                     ubicacion_entry.get(),
                                     edit_window
                                 ))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def edit_categoria(self, idcategoria, nombre_categoria, ubicacion, window):
        if nombre_categoria and ubicacion:
            self.execute_query('''
                UPDATE categorias
                SET NOMBRE_CATEGORIA = ?, UBICACION = ?
                WHERE idcategoria = ?
            ''', (nombre_categoria, ubicacion, idcategoria))
            messagebox.showinfo("Éxito", "Categoría editada correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def delete_categoria(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta categoría?")
        if confirm:
            self.execute_query('DELETE FROM categorias WHERE idcategoria = ?', (values[0],))
            messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
            self.populate_tree()

    def convert_to_excel(self):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categorias')
        categorias = cursor.fetchall()
        connection.close()

        columns = ['ID', 'Nombre Categoría', 'Ubicación']
        df = pd.DataFrame(categorias, columns=columns)
        df.to_excel('categorias.xlsx', index=False)
        messagebox.showinfo("Éxito", "Datos exportados a Excel correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Categorías")
    app = CategoriasApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()

