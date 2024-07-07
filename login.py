import tkinter as tk
from tkinter import messagebox

# Credenciales de usuario (esto debería almacenarse de manera segura)
CREDENTIALS = {
    "admin": {"password": "1234", "role": "admin"},
    "estudiante": {"password": "1234", "role": "estudiante"},
    "biblio": {"password": "1234", "role": "bibliotecario"}  # Nuevo rol de bibliotecario
}

class LoginApp(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title('Login')
        self.geometry('300x300')

        self.label_id_usuario = tk.Label(self, text='ID de Usuario:')
        self.label_id_usuario.pack(pady=5)
        self.entry_id_usuario = tk.Entry(self)
        self.entry_id_usuario.pack(pady=5)

        self.label_password = tk.Label(self, text='Contraseña:')
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show='*')
        self.entry_password.pack(pady=5)

        self.label_role = tk.Label(self, text='Selecciona tu rol:')
        self.label_role.pack(pady=5)
        
        self.role_var = tk.StringVar(value="admin")
        self.radio_admin = tk.Radiobutton(self, text='Admin', variable=self.role_var, value='admin')
        self.radio_admin.pack(pady=2)
        self.radio_estudiante = tk.Radiobutton(self, text='Estudiante', variable=self.role_var, value='estudiante')
        self.radio_estudiante.pack(pady=2)
        self.radio_bibliotecario = tk.Radiobutton(self, text='Bibliotecario', variable=self.role_var, value='bibliotecario')
        self.radio_bibliotecario.pack(pady=2)

        self.boton_login = tk.Button(self, text='Login', command=self.verificar_credenciales)
        self.boton_login.pack(pady=10)

    def verificar_credenciales(self):
        id_usuario = self.entry_id_usuario.get()
        password = self.entry_password.get()
        role = self.role_var.get()

        if id_usuario in CREDENTIALS and CREDENTIALS[id_usuario]["password"] == password and CREDENTIALS[id_usuario]["role"] == role:
            messagebox.showinfo('Login', 'Credenciales correctas')
            self.master.login_successful(id_usuario, role)
            self.destroy()
        else:
            messagebox.showerror('Login', 'ID de usuario, contraseña o rol incorrectos')

# Ejemplo de uso
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application")

        self.login_window = None
        self.open_login_window()

    def open_login_window(self):
        self.withdraw()  # Ocultar la ventana principal mientras se muestra la ventana de login
        self.login_window = LoginApp(self)
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_login_window_close)

    def on_login_window_close(self):
        self.login_window.destroy()
        self.login_window = None
        self.deiconify()  # Mostrar nuevamente la ventana principal

    def login_successful(self, id_usuario, role):
        # Aquí implementarías lo que sucede después de un login exitoso
        print(f"Login exitoso. ID: {id_usuario}, Rol: {role}")
        # Por ejemplo, podrías abrir otra ventana o realizar alguna acción específica.

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
