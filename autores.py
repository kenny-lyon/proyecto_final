import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class AutoresApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)

        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_autor)
        search_button.pack(side=tk.LEFT, padx=5)

        # Botón para mostrar todos los registros
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_autores)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botón para convertir a Excel
        convert_button = ttk.Button(search_frame, text="Convertir a Excel", command=self.convert_to_excel)
        convert_button.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self, columns=('idautor', 'NOMBRES', 'APELLIDOS', 'DNI', 'MODALIDAD', 'AUTORESCOL'), show='headings')
        self.tree.heading('idautor', text='ID')
        self.tree.heading('NOMBRES', text='Nombres')
        self.tree.heading('APELLIDOS', text='Apellidos')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('MODALIDAD', text='Modalidad')
        self.tree.heading('AUTORESCOL', text='Autorescol')
        self.tree.pack(expand=True, fill='both')

        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_autor_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_autor_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_autor)

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
                SELECT * FROM autores 
                WHERE NOMBRES LIKE ? OR APELLIDOS LIKE ? OR DNI LIKE ? OR MODALIDAD LIKE ? OR AUTORESCOL LIKE ?
            ''', ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute('SELECT * FROM autores')
        autores = cursor.fetchall()
        for autor in autores:
            self.tree.insert('', tk.END, values=autor)
        connection.close()

    def open_add_autor_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("Agregar Autor")

        form_frame = ttk.Frame(new_window)
        form_frame.pack(pady=10, padx=10)

        nombres_label = ttk.Label(form_frame, text="Nombres:")
        nombres_label.grid(row=0, column=0)
        nombres_entry = ttk.Entry(form_frame)
        nombres_entry.grid(row=0, column=1)

        apellidos_label = ttk.Label(form_frame, text="Apellidos:")
        apellidos_label.grid(row=1, column=0)
        apellidos_entry = ttk.Entry(form_frame)
        apellidos_entry.grid(row=1, column=1)

        dni_label = ttk.Label(form_frame, text="DNI:")
        dni_label.grid(row=2, column=0)
        dni_entry = ttk.Entry(form_frame)
        dni_entry.grid(row=2, column=1)

        modalidad_label = ttk.Label(form_frame, text="Modalidad:")
        modalidad_label.grid(row=3, column=0)
        modalidad_entry = ttk.Entry(form_frame)
        modalidad_entry.grid(row=3, column=1)

        autorescol_label = ttk.Label(form_frame, text="Autorescol:")
        autorescol_label.grid(row=4, column=0)
        autorescol_entry = ttk.Entry(form_frame)
        autorescol_entry.grid(row=4, column=1)

        add_button = ttk.Button(form_frame, text="Agregar", 
                                command=lambda: self.add_autor(
                                    nombres_entry.get(),
                                    apellidos_entry.get(),
                                    dni_entry.get(),
                                    modalidad_entry.get(),
                                    autorescol_entry.get(),
                                    new_window
                                ))
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def add_autor(self, nombres, apellidos, dni, modalidad, autorescol, window):
        if nombres and apellidos and dni and modalidad and autorescol:
            self.execute_query('''
                INSERT INTO autores (NOMBRES, APELLIDOS, DNI, MODALIDAD, AUTORESCOL) 
                VALUES (?, ?, ?, ?, ?)
            ''', (nombres, apellidos, dni, modalidad, autorescol))
            messagebox.showinfo("Éxito", "Autor agregado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def search_autor(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_autores(self):
        self.search_entry.delete(0, tk.END)
        self.populate_tree()

    def show_context_menu(self, event):
        self.selected_item = self.tree.identify_row(event.y)
        if self.selected_item:
            self.tree.selection_set(self.selected_item)
            self.context_menu.post(event.x_root, event.y_root)

    def open_edit_autor_window(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Autor")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="Nombres:").grid(row=0, column=0)
        nombres_entry = ttk.Entry(form_frame)
        nombres_entry.insert(0, values[1])
        nombres_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Apellidos:").grid(row=1, column=0)
        apellidos_entry = ttk.Entry(form_frame)
        apellidos_entry.insert(0, values[2])
        apellidos_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="DNI:").grid(row=2, column=0)
        dni_entry = ttk.Entry(form_frame)
        dni_entry.insert(0, values[3])
        dni_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Modalidad:").grid(row=3, column=0)
        modalidad_entry = ttk.Entry(form_frame)
        modalidad_entry.insert(0, values[4])
        modalidad_entry.grid(row=3, column=1)

        ttk.Label(form_frame, text="Autorescol:").grid(row=4, column=0)
        autorescol_entry = ttk.Entry(form_frame)
        autorescol_entry.insert(0, values[5])
        autorescol_entry.grid(row=4, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.edit_autor(
                                     values[0],
                                     nombres_entry.get(),
                                     apellidos_entry.get(),
                                     dni_entry.get(),
                                     modalidad_entry.get(),
                                     autorescol_entry.get(),
                                     edit_window
                                 ))
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_autor(self, idautor, nombres, apellidos, dni, modalidad, autorescol, window):
        if nombres and apellidos and dni and modalidad and autorescol:
            self.execute_query('''
                UPDATE autores
                SET NOMBRES = ?, APELLIDOS = ?, DNI = ?, MODALIDAD = ?, AUTORESCOL = ?
                WHERE idautor = ?
            ''', (nombres, apellidos, dni, modalidad, autorescol, idautor))
            messagebox.showinfo("Éxito", "Autor editado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def delete_autor(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este autor?")
        if confirm:
            self.execute_query('DELETE FROM autores WHERE idautor = ?', (values[0],))
            messagebox.showinfo("Éxito", "Autor eliminado correctamente")
            self.populate_tree()       

    def convert_to_excel(self):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM autores')
        autores = cursor.fetchall()
        connection.close()

        columns = ['ID', 'Nombres', 'Apellidos', 'DNI', 'Modalidad', 'Autorescol']
        df = pd.DataFrame(autores, columns=columns)
        df.to_excel('autores.xlsx', index=False)
        messagebox.showinfo("Éxito", "Datos exportados a Excel correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Autores")
    app = AutoresApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
