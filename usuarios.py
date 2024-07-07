import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class UsuariosApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)
        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_usuario)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Agregar botón para mostrar todos los usuarios
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_usuarios)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botón para convertir a Excel
        convert_button = ttk.Button(search_frame, text="Convertir a Excel", command=self.export_to_excel)
        convert_button.pack(side=tk.RIGHT, padx=5)

        # Botón para importar desde Excel
        import_button = ttk.Button(search_frame, text="Importar desde Excel", command=self.import_from_excel)
        import_button.pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=('idusuario', 'DNI', 'NOMBRES', 'APELLIDOS', 'PASSWORD', 'DIRECCION', 'CELULAR'), show='headings')
        self.tree.heading('idusuario', text='ID')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('NOMBRES', text='Nombres')
        self.tree.heading('APELLIDOS', text='Apellidos')
        self.tree.heading('PASSWORD', text='Password')
        self.tree.heading('DIRECCION', text='Dirección')
        self.tree.heading('CELULAR', text='Celular')
        self.tree.pack(expand=True, fill='both')

        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_usuario_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_usuario)

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
            cursor.execute('SELECT * FROM usuarios WHERE NOMBRES LIKE ? OR APELLIDOS LIKE ?', ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            self.tree.insert('', tk.END, values=usuario)
        connection.close()

    def add_usuario(self, dni, nombres, apellidos, password, direccion, celular):
        if dni and nombres and apellidos and password and direccion and celular:
            self.execute_query('''
                INSERT INTO usuarios (DNI, NOMBRES, APELLIDOS, PASSWORD, DIRECCION, CELULAR) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (dni, nombres, apellidos, password, direccion, celular))
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def open_add_usuario_window(self):
        add_usuario_window = tk.Toplevel(self)
        add_usuario_window.title("Agregar Usuario")

        ttk.Label(add_usuario_window, text="DNI:").grid(row=0, column=0, padx=10, pady=10)
        dni_entry = ttk.Entry(add_usuario_window)
        dni_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(add_usuario_window, text="Nombres:").grid(row=1, column=0, padx=10, pady=10)
        nombres_entry = ttk.Entry(add_usuario_window)
        nombres_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(add_usuario_window, text="Apellidos:").grid(row=2, column=0, padx=10, pady=10)
        apellidos_entry = ttk.Entry(add_usuario_window)
        apellidos_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(add_usuario_window, text="Password:").grid(row=3, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(add_usuario_window)
        password_entry.grid(row=3, column=1, padx=10, pady=10)
        
        ttk.Label(add_usuario_window, text="Dirección:").grid(row=4, column=0, padx=10, pady=10)
        direccion_entry = ttk.Entry(add_usuario_window)
        direccion_entry.grid(row=4, column=1, padx=10, pady=10)
        
        ttk.Label(add_usuario_window, text="Celular:").grid(row=5, column=0, padx=10, pady=10)
        celular_entry = ttk.Entry(add_usuario_window)
        celular_entry.grid(row=5, column=1, padx=10, pady=10)
        
        save_button = ttk.Button(add_usuario_window, text="Guardar", 
                                 command=lambda: self.save_usuario(
                                     add_usuario_window,
                                     dni_entry.get(),
                                     nombres_entry.get(),
                                     apellidos_entry.get(),
                                     password_entry.get(),
                                     direccion_entry.get(),
                                     celular_entry.get()
                                 ))
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_usuario(self, window, dni, nombres, apellidos, password, direccion, celular):
        self.add_usuario(dni, nombres, apellidos, password, direccion, celular)
        window.destroy()

    def search_usuario(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_usuarios(self):
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
        edit_window.title("Editar Usuario")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="DNI:").grid(row=0, column=0)
        dni_entry = ttk.Entry(form_frame)
        dni_entry.insert(0, values[1])
        dni_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Nombres:").grid(row=1, column=0)
        nombres_entry = ttk.Entry(form_frame)
        nombres_entry.insert(0, values[2])
        nombres_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Apellidos:").grid(row=2, column=0)
        apellidos_entry = ttk.Entry(form_frame)
        apellidos_entry.insert(0, values[3])
        apellidos_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Password:").grid(row=3, column=0)
        password_entry = ttk.Entry(form_frame)
        password_entry.insert(0, values[4])
        password_entry.grid(row=3, column=1)

        ttk.Label(form_frame, text="Dirección:").grid(row=4, column=0)
        direccion_entry = ttk.Entry(form_frame)
        direccion_entry.insert(0, values[5])
        direccion_entry.grid(row=4, column=1)

        ttk.Label(form_frame, text="Celular:").grid(row=5, column=0)
        celular_entry = ttk.Entry(form_frame)
        celular_entry.insert(0, values[6])
        celular_entry.grid(row=5, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.edit_usuario(
                                     values[0],
                                     dni_entry.get(),
                                     nombres_entry.get(),
                                     apellidos_entry.get(),
                                     password_entry.get(),
                                     direccion_entry.get(),
                                     celular_entry.get(),
                                     edit_window
                                 ))
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def edit_usuario(self, idusuario, dni, nombres, apellidos, password, direccion, celular, window):
        if dni and nombres and apellidos and password and direccion and celular:
            self.execute_query('''
                UPDATE usuarios
                SET DNI = ?, NOMBRES = ?, APELLIDOS = ?, PASSWORD = ?, DIRECCION = ?, CELULAR = ?
                WHERE idusuario = ?
            ''', (dni, nombres, apellidos, password, direccion, celular, idusuario))
            messagebox.showinfo("Éxito", "Usuario editado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def delete_usuario(self):
        item = self.tree.item(self.selected_item)
        idusuario = item['values'][0]
        
        if messagebox.askyesno("Confirmar eliminación", "¿Estás seguro que deseas eliminar este usuario?"):
            self.execute_query('DELETE FROM usuarios WHERE idusuario = ?', (idusuario,))
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            self.populate_tree()

    def export_to_excel(self):
        filename = "usuarios.xlsx"  # Nombre predeterminado del archivo
        try:
            usuarios_data = []
            for item in self.tree.get_children():
                usuarios_data.append(self.tree.item(item)['values'])

            df = pd.DataFrame(usuarios_data, columns=['ID', 'DNI', 'Nombres', 'Apellidos', 'Password', 'Dirección', 'Celular'])
            df.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {str(e)}")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if 'DNI' in df.columns and 'Nombres' in df.columns and 'Apellidos' in df.columns and 'Password' in df.columns and 'Dirección' in df.columns and 'Celular' in df.columns:
                    for index, row in df.iterrows():
                        self.execute_query('''
                            INSERT INTO usuarios (DNI, NOMBRES, APELLIDOS, PASSWORD, DIRECCION, CELULAR) 
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (row['DNI'], row['Nombres'], row['Apellidos'], row['Password'], row['Dirección'], row['Celular']))
                    messagebox.showinfo("Éxito", "Datos importados correctamente desde Excel")
                    self.populate_tree()
                else:
                    messagebox.showerror("Error", "El archivo Excel no tiene las columnas necesarias")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al importar desde Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Usuarios")
    app = UsuariosApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
