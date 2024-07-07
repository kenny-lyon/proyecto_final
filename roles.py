import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class RolesApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)
        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_rol)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Agregar botón para mostrar todos los roles
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_roles)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botón para convertir a Excel
        convert_button = ttk.Button(search_frame, text="Convertir a Excel", command=self.export_to_excel)
        convert_button.pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=('idrol', 'NOMBRE'), show='headings')
        self.tree.heading('idrol', text='ID')
        self.tree.heading('NOMBRE', text='Nombre')
        self.tree.pack(expand=True, fill='both')

        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_rol_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_rol)

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
            cursor.execute('SELECT * FROM roles WHERE NOMBRE LIKE ?', ('%' + search_term + '%',))
        else:
            cursor.execute('SELECT * FROM roles')
        roles = cursor.fetchall()
        for rol in roles:
            self.tree.insert('', tk.END, values=rol)
        connection.close()

    def add_rol(self, nombre):
        if nombre:
            self.execute_query('''
                INSERT INTO roles (NOMBRE) 
                VALUES (?)
            ''', (nombre,))
            messagebox.showinfo("Éxito", "Rol agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "El campo nombre es obligatorio")

    def open_add_rol_window(self):
        add_rol_window = tk.Toplevel(self)
        add_rol_window.title("Agregar Rol")

        nombre_label = ttk.Label(add_rol_window, text="Nombre:")
        nombre_label.grid(row=0, column=0, padx=10, pady=10)
        
        nombre_entry = ttk.Entry(add_rol_window)
        nombre_entry.grid(row=0, column=1, padx=10, pady=10)
        
        save_button = ttk.Button(add_rol_window, text="Guardar", command=lambda: self.save_rol(add_rol_window, nombre_entry.get()))
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def save_rol(self, window, nombre):
        self.add_rol(nombre)
        window.destroy()

    def search_rol(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_roles(self):
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
        edit_window.title("Editar Rol")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0)
        nombre_entry = ttk.Entry(form_frame)
        nombre_entry.insert(0, values[1])
        nombre_entry.grid(row=0, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.edit_rol(
                                     values[0],
                                     nombre_entry.get(),
                                     edit_window
                                 ))
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def edit_rol(self, idrol, nombre, window):
        if nombre:
            self.execute_query('''
                UPDATE roles
                SET NOMBRE = ?
                WHERE idrol = ?
            ''', (nombre, idrol))
            messagebox.showinfo("Éxito", "Rol editado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "El campo nombre es obligatorio")

    def delete_rol(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este rol?")
        if confirm:
            self.execute_query('DELETE FROM roles WHERE idrol = ?', (values[0],))
            messagebox.showinfo("Éxito", "Rol eliminado correctamente")
            self.populate_tree()

    def export_to_excel(self):
        filename = "roles.xlsx"  # Nombre predeterminado del archivo
        try:
            roles_data = []
            for item in self.tree.get_children():
                roles_data.append(self.tree.item(item)['values'])

            df = pd.DataFrame(roles_data, columns=['ID', 'Nombre'])
            df.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Roles")
    app = RolesApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
