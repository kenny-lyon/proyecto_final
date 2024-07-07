import tkinter as tk
from tkinter import ttk
from login import LoginApp
from autores import AutoresApp
from categorias import CategoriasApp
from libros import LibrosApp
from libros_autores import LibrosAutoresApp
from prestamos import PrestamosApp
from usuarios import UsuariosApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # Ocultar la ventana principal hasta que se pase el login
        self.title("Biblioteca")
        self.geometry("700x400")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.after(0, self.show_login)

    def show_login(self):
        login_window = LoginApp(self)
        login_window.grab_set()

    def login_successful(self, user_id, role):
        self.deiconify()  # Mostrar la ventana principal
        self.user_id = user_id
        self.role = role

        self.label_user_info = tk.Label(self, text=f"Usuario: {self.user_id} - Rol: {self.role}")
        self.label_user_info.pack(pady=10)

        if self.role == "admin":
            self.autores_app = AutoresApp(self.notebook)
            self.notebook.add(self.autores_app, text="Autores")

            self.categorias_app = CategoriasApp(self.notebook)
            self.notebook.add(self.categorias_app, text="Categorías")

            self.libros_app = LibrosApp(self.notebook)
            self.notebook.add(self.libros_app, text="Libros")

            self.libros_autores_app = LibrosAutoresApp(self.notebook)
            self.notebook.add(self.libros_autores_app, text="Libros y Autores")

            self.prestamos_app = PrestamosApp(self.notebook)
            self.notebook.add(self.prestamos_app, text="Préstamos")

            self.usuarios_app = UsuariosApp(self.notebook)
            self.notebook.add(self.usuarios_app, text="Usuarios")
        else:
            self.libros_app = LibrosApp(self.notebook)
            self.notebook.add(self.libros_app, text="Libros")

            self.prestamos_app = PrestamosApp(self.notebook)
            self.notebook.add(self.prestamos_app, text="Préstamos")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
