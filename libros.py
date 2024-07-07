import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class LibrosApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)
        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_libro)
        search_button.pack(side=tk.LEFT, padx=5)

        # Botón para mostrar todos los registros
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_libros)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botón para convertir a Excel
        convert_button = ttk.Button(search_frame, text="Convertir a Excel", command=self.export_to_excel)
        convert_button.pack(side=tk.RIGHT, padx=5)

        # Botón para importar desde Excel
        import_button = ttk.Button(search_frame, text="Importar desde Excel", command=self.import_from_excel)
        import_button.pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=('idlibro', 'TITULO', 'AUTORES', 'EDICION', 'DESCRIPCION', 'AÑO', 'NUMEROPAGINAS', 'CATEGORIA_IDCATEGORIA'), show='headings')
        self.tree.heading('idlibro', text='ID')
        self.tree.heading('TITULO', text='Título')
        self.tree.heading('AUTORES', text='Autores')
        self.tree.heading('EDICION', text='Edición')
        self.tree.heading('DESCRIPCION', text='Descripción')
        self.tree.heading('AÑO', text='Año')
        self.tree.heading('NUMEROPAGINAS', text='Número de Páginas')
        self.tree.heading('CATEGORIA_IDCATEGORIA', text='ID Categoría')
        self.tree.pack(expand=True, fill='both')

        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_libro)

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
                SELECT * FROM libros 
                WHERE TITULO LIKE ? OR AUTORES LIKE ? OR EDICION LIKE ? OR DESCRIPCION LIKE ? OR AÑO LIKE ? OR NUMEROPAGINAS LIKE ? OR CATEGORIA_IDCATEGORIA LIKE ?
            ''', ('%' + search_term + '%',) * 7)
        else:
            cursor.execute('SELECT * FROM libros')
        libros = cursor.fetchall()
        for libro in libros:
            self.tree.insert('', tk.END, values=libro)
        connection.close()

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar Libro")

        form_frame = ttk.Frame(add_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="Título:").grid(row=0, column=0)
        titulo_entry = ttk.Entry(form_frame)
        titulo_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Autores:").grid(row=1, column=0)
        autores_entry = ttk.Entry(form_frame)
        autores_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Edición:").grid(row=2, column=0)
        edicion_entry = ttk.Entry(form_frame)
        edicion_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Descripción:").grid(row=3, column=0)
        descripcion_entry = ttk.Entry(form_frame)
        descripcion_entry.grid(row=3, column=1)

        ttk.Label(form_frame, text="Año:").grid(row=4, column=0)
        año_entry = ttk.Entry(form_frame)
        año_entry.grid(row=4, column=1)

        ttk.Label(form_frame, text="Número de Páginas:").grid(row=5, column=0)
        numeropaginas_entry = ttk.Entry(form_frame)
        numeropaginas_entry.grid(row=5, column=1)

        ttk.Label(form_frame, text="ID Categoría:").grid(row=6, column=0)
        categoria_idcategoria_entry = ttk.Entry(form_frame)
        categoria_idcategoria_entry.grid(row=6, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.add_libro(
                                     titulo_entry.get(),
                                     autores_entry.get(),
                                     edicion_entry.get(),
                                     descripcion_entry.get(),
                                     año_entry.get(),
                                     numeropaginas_entry.get(),
                                     categoria_idcategoria_entry.get(),
                                     add_window
                                 ))
        save_button.grid(row=7, column=0, columnspan=2, pady=10)

    def add_libro(self, titulo, autores, edicion, descripcion, año, numeropaginas, categoria_idcategoria, window):
        if titulo and autores and edicion and descripcion and año and numeropaginas and categoria_idcategoria:
            self.execute_query('''
                INSERT INTO libros (TITULO, AUTORES, EDICION, DESCRIPCION, AÑO, NUMEROPAGINAS, CATEGORIA_IDCATEGORIA) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, autores, edicion, descripcion, año, numeropaginas, categoria_idcategoria))
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def search_libro(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_libros(self):
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
        edit_window.title("Editar Libro")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="Título:").grid(row=0, column=0)
        titulo_entry = ttk.Entry(form_frame)
        titulo_entry.insert(0, values[1])
        titulo_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Autores:").grid(row=1, column=0)
        autores_entry = ttk.Entry(form_frame)
        autores_entry.insert(0, values[2])
        autores_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Edición:").grid(row=2, column=0)
        edicion_entry = ttk.Entry(form_frame)
        edicion_entry.insert(0, values[3])
        edicion_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Descripción:").grid(row=3, column=0)
        descripcion_entry = ttk.Entry(form_frame)
        descripcion_entry.insert(0, values[4])
        descripcion_entry.grid(row=3, column=1)

        ttk.Label(form_frame, text="Año:").grid(row=4, column=0)
        año_entry = ttk.Entry(form_frame)
        año_entry.insert(0, values[5])
        año_entry.grid(row=4, column=1)

        ttk.Label(form_frame, text="Número de Páginas:").grid(row=5, column=0)
        numeropaginas_entry = ttk.Entry(form_frame)
        numeropaginas_entry.insert(0, values[6])
        numeropaginas_entry.grid(row=5, column=1)

        ttk.Label(form_frame, text="ID Categoría:").grid(row=6, column=0)
        categoria_idcategoria_entry = ttk.Entry(form_frame)
        categoria_idcategoria_entry.insert(0, values[7])
        categoria_idcategoria_entry.grid(row=6, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.edit_libro(
                                     values[0],
                                     titulo_entry.get(),
                                     autores_entry.get(),
                                     edicion_entry.get(),
                                     descripcion_entry.get(),
                                     año_entry.get(),
                                     numeropaginas_entry.get(),
                                     categoria_idcategoria_entry.get(),
                                     edit_window
                                 ))
        save_button.grid(row=7, column=0, columnspan=2, pady=10)

    def edit_libro(self, idlibro, titulo, autores, edicion, descripcion, año, numeropaginas, categoria_idcategoria, window):
        if titulo and autores and edicion and descripcion and año and numeropaginas and categoria_idcategoria:
            self.execute_query('''
                UPDATE libros
                SET TITULO = ?, AUTORES = ?, EDICION = ?, DESCRIPCION = ?, AÑO = ?, NUMEROPAGINAS = ?, CATEGORIA_IDCATEGORIA = ?
                WHERE idlibro = ?
            ''', (titulo, autores, edicion, descripcion, año, numeropaginas, categoria_idcategoria, idlibro))
            messagebox.showinfo("Éxito", "Libro editado correctamente")
            self.populate_tree()
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def delete_libro(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este libro?")
        if confirm:
            self.execute_query('DELETE FROM libros WHERE idlibro = ?', (values[0],))
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            self.populate_tree()

    def export_to_excel(self):
        filename = "libros.xlsx"  # Nombre predeterminado del archivo
        try:
            libros_data = []
            for item in self.tree.get_children():
                libros_data.append(self.tree.item(item)['values'])

            df = pd.DataFrame(libros_data, columns=['ID', 'Título', 'Autores', 'Edición', 'Descripción', 'Año', 'Número de Páginas', 'ID Categoría'])
            df.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a '{filename}' correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {str(e)}")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if 'Título' in df.columns and 'Autores' in df.columns and 'Edición' in df.columns and 'Descripción' in df.columns and 'Año' in df.columns and 'Número de Páginas' in df.columns and 'ID Categoría' in df.columns:
                    for index, row in df.iterrows():
                        self.execute_query('''
                            INSERT INTO libros (TITULO, AUTORES, EDICION, DESCRIPCION, AÑO, NUMEROPAGINAS, CATEGORIA_IDCATEGORIA) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (row['Título'], row['Autores'], row['Edición'], row['Descripción'], row['Año'], row['Número de Páginas'], row['ID Categoría']))
                    messagebox.showinfo("Éxito", "Datos importados correctamente desde Excel")
                    self.populate_tree()
                else:
                    messagebox.showerror("Error", "El archivo Excel no tiene las columnas necesarias")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al importar desde Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Libros")
    app = LibrosApp(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
