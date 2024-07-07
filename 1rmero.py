import tkinter as tk
from tkinter import messagebox
import sqlite3

# Credenciales de usuario
USER_ID = "76645011"
PASSWORD = "29052005"

def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width=300, height=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='usuario', menu=menu_inicio)

    menu_inicio.add_command(label='crear un registro en BD', command=lambda: habilitar_campos(root))
    menu_inicio.add_command(label='eliminar registro en BD')
    menu_inicio.add_command(label='salir', command=root.destroy)

    menu_prestamos = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='prestamos', menu=menu_prestamos)
    menu_prestamos.add_command(label='Registrar Préstamo', command=ventana_prestamo)

    barra_menu.add_cascade(label='libros')
    barra_menu.add_cascade(label='autores')

def habilitar_campos(root):
    for widget in root.winfo_children():
        if isinstance(widget, Frame):
            widget.habilitar_campos()

def ventana_prestamo():
    ventana = tk.Toplevel()
    ventana.title('Registrar Préstamo')
    ventana.geometry('400x300')

    # Labels y Entrys para los campos de préstamo
    label_fecha_prestamo = tk.Label(ventana, text='Fecha de Préstamo:')
    label_fecha_prestamo.grid(row=0, column=0, padx=10, pady=10)
    entry_fecha_prestamo = tk.Entry(ventana)
    entry_fecha_prestamo.grid(row=0, column=1, padx=10, pady=10)

    label_fecha_entrega = tk.Label(ventana, text='Fecha de Entrega:')
    label_fecha_entrega.grid(row=1, column=0, padx=10, pady=10)
    entry_fecha_entrega = tk.Entry(ventana)
    entry_fecha_entrega.grid(row=1, column=1, padx=10, pady=10)

    label_libro = tk.Label(ventana, text='Libro:')
    label_libro.grid(row=2, column=0, padx=10, pady=10)
    entry_libro = tk.Entry(ventana)
    entry_libro.grid(row=2, column=1, padx=10, pady=10)

    label_id_usuario = tk.Label(ventana, text='ID de Usuario:')
    label_id_usuario.grid(row=3, column=0, padx=10, pady=10)
    entry_id_usuario = tk.Entry(ventana)
    entry_id_usuario.grid(row=3, column=1, padx=10, pady=10)

    def guardar_prestamo():
        fecha_prestamo = entry_fecha_prestamo.get()
        fecha_entrega = entry_fecha_entrega.get()
        libro = entry_libro.get()
        id_usuario = entry_id_usuario.get()

        if fecha_prestamo and fecha_entrega and libro and id_usuario:
            cursor.execute('''
                INSERT INTO prestamos (fecha_prestamo, fecha_entrega, libro, id_usuario)
                VALUES (?, ?, ?, ?)
            ''', (fecha_prestamo, fecha_entrega, libro, id_usuario))
            conn.commit()
            messagebox.showinfo('Guardar', 'Préstamo registrado con éxito')
            ventana.destroy()
        else:
            messagebox.showwarning('Advertencia', 'Todos los campos son obligatorios')

    boton_guardar = tk.Button(ventana, text='Guardar', command=guardar_prestamo)
    boton_guardar.grid(row=4, column=0, columnspan=2, pady=10)

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack()
        self.conectar_db()
        self.campos_usuario()
        self.deshabilitar_campos()
        self.resultados = tk.Listbox(self)
        self.resultados.grid(row=7, column=0, columnspan=3, sticky="nsew")
        self.resultados.config(width=50, height=10, font=('Arial', 12))
        self.resultados.bind("<Button-3>", self.mostrar_menu_contextual)
        self.menu_contextual = tk.Menu(self.resultados, tearoff=0)
        self.menu_contextual.add_command(label="Editar", command=self.editar_registro)
        self.menu_contextual.add_command(label="Eliminar", command=self.eliminar_registro)
        self.mostrar_datos()

    def conectar_db(self):
        global conn, cursor
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                duracion TEXT NOT NULL,
                genero TEXT NOT NULL,
                id_usuario TEXT NOT NULL,
                dni TEXT NOT NULL,
                direccion TEXT NOT NULL,
                celular TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_prestamo TEXT NOT NULL,
                fecha_entrega TEXT NOT NULL,
                libro TEXT NOT NULL,
                id_usuario TEXT NOT NULL
            )
        ''')
        conn.commit()

    def campos_usuario(self):
        # Labels de cada campo
        self.label_nombre = tk.Label(self, text='Nombre:')
        self.label_nombre.config(font=('Arial', 12, 'bold'))
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.label_duracion = tk.Label(self, text='Duracion:')
        self.label_duracion.config(font=('Arial', 12, 'bold'))
        self.label_duracion.grid(row=1, column=0, padx=10, pady=10)

        self.label_genero = tk.Label(self, text='Genero:')
        self.label_genero.config(font=('Arial', 12, 'bold'))
        self.label_genero.grid(row=2, column=0, padx=10, pady=10)

        self.label_id_usuario = tk.Label(self, text='ID Usuario:')
        self.label_id_usuario.config(font=('Arial', 12, 'bold'))
        self.label_id_usuario.grid(row=3, column=0, padx=10, pady=10)

        self.label_dni = tk.Label(self, text='DNI:')
        self.label_dni.config(font=('Arial', 12, 'bold'))
        self.label_dni.grid(row=4, column=0, padx=10, pady=10)

        self.label_direccion = tk.Label(self, text='Direccion:')
        self.label_direccion.config(font=('Arial', 12, 'bold'))
        self.label_direccion.grid(row=5, column=0, padx=10, pady=10)

        self.label_celular = tk.Label(self, text='Celular:')
        self.label_celular.config(font=('Arial', 12, 'bold'))
        self.label_celular.grid(row=6, column=0, padx=10, pady=10)

        self.label_rol = tk.Label(self, text='Rol:')
        self.label_rol.config(font=('Arial', 12, 'bold'))
        self.label_rol.grid(row=7, column=0, padx=10, pady=10)

        # Entrys de cada campo
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=50, font=('Arial', 12))
        self.entry_nombre.grid(row=0, column=1, columnspan=2)

        self.mi_duracion = tk.StringVar()
        self.entry_duracion = tk.Entry(self, textvariable=self.mi_duracion)
        self.entry_duracion.config(width=50, font=('Arial', 12))
        self.entry_duracion.grid(row=1, column=1, columnspan=2)

        self.mi_genero = tk.StringVar()
        self.entry_genero = tk.Entry(self, textvariable=self.mi_genero)
        self.entry_genero.config(width=50, font=('Arial', 12))
        self.entry_genero.grid(row=2, column=1, columnspan=2)

        self.mi_id_usuario = tk.StringVar()
        self.entry_id_usuario = tk.Entry(self, textvariable=self.mi_id_usuario)
        self.entry_id_usuario.config(width=50, font=('Arial', 12))
        self.entry_id_usuario.grid(row=3, column=1, columnspan=2)

        self.mi_dni = tk.StringVar()
        self.entry_dni = tk.Entry(self, textvariable=self.mi_dni)
        self.entry_dni.config(width=50, font=('Arial', 12))
        self.entry_dni.grid(row=4, column=1, columnspan=2)

        self.mi_direccion = tk.StringVar()
        self.entry_direccion = tk.Entry(self, textvariable=self.mi_direccion)
        self.entry_direccion.config(width=50, font=('Arial', 12))
        self.entry_direccion.grid(row=5, column=1, columnspan=2)

        self.mi_celular = tk.StringVar()
        self.entry_celular = tk.Entry(self, textvariable=self.mi_celular)
        self.entry_celular.config(width=50, font=('Arial', 12))
        self.entry_celular.grid(row=6, column=1, columnspan=2)

        self.mi_rol = tk.StringVar()
        self.entry_rol = tk.Entry(self, textvariable=self.mi_rol)
        self.entry_rol.config(width=50, font=('Arial', 12))
        self.entry_rol.grid(row=7, column=1, columnspan=2)

        # Botones
        self.boton_nuevo = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#158645', cursor='hand2', activebackground='#35BD6F')
        self.boton_nuevo.grid(row=8, column=0, padx=10, pady=10)

        self.boton_guardar = tk.Button(self, text='Guardar', command=self.guardar_datos)
        self.boton_guardar.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#1658A2', cursor='hand2', activebackground='#3586DF')
        self.boton_guardar.grid(row=8, column=1, padx=10, pady=10)

        self.boton_cancelar = tk.Button(self, text='Cancelar', command=self.deshabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#BD152E', cursor='hand2', activebackground='#E15370')
        self.boton_cancelar.grid(row=8, column=2, padx=10, pady=10)

    def habilitar_campos(self):
        self.mi_nombre.set('')
        self.mi_duracion.set('')
        self.mi_genero.set('')
        self.mi_id_usuario.set('')
        self.mi_dni.set('')
        self.mi_direccion.set('')
        self.mi_celular.set('')
        self.mi_rol.set('')

        self.entry_nombre.config(state='normal')
        self.entry_duracion.config(state='normal')
        self.entry_genero.config(state='normal')
        self.entry_id_usuario.config(state='normal')
        self.entry_dni.config(state='normal')
        self.entry_direccion.config(state='normal')
        self.entry_celular.config(state='normal')
        self.entry_rol.config(state='normal')

        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def deshabilitar_campos(self):
        self.mi_nombre.set('')
        self.mi_duracion.set('')
        self.mi_genero.set('')
        self.mi_id_usuario.set('')
        self.mi_dni.set('')
        self.mi_direccion.set('')
        self.mi_celular.set('')
        self.mi_rol.set('')

        self.entry_nombre.config(state='disabled')
        self.entry_duracion.config(state='disabled')
        self.entry_genero.config(state='disabled')
        self.entry_id_usuario.config(state='disabled')
        self.entry_dni.config(state='disabled')
        self.entry_direccion.config(state='disabled')
        self.entry_celular.config(state='disabled')
        self.entry_rol.config(state='disabled')

        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

    def guardar_datos(self):
        datos = (self.mi_nombre.get(), self.mi_duracion.get(), self.mi_genero.get(), self.mi_id_usuario.get(), self.mi_dni.get(), self.mi_direccion.get(), self.mi_celular.get(), self.mi_rol.get())
        cursor.execute('''
            INSERT INTO usuarios (nombre, duracion, genero, id_usuario, dni, direccion, celular, rol)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', datos)
        conn.commit()
        messagebox.showinfo('Guardar', 'Datos guardados con éxito')
        self.deshabilitar_campos()
        self.mostrar_datos()

    def mostrar_datos(self):
        cursor.execute('SELECT * FROM usuarios')
        registros = cursor.fetchall()
        self.resultados.delete(0, tk.END)
        for registro in registros:
            self.resultados.insert(tk.END, registro)

    def mostrar_menu_contextual(self, event):
        self.menu_contextual.post(event.x_root, event.y_root)

    def editar_registro(self):
        seleccion = self.resultados.curselection()
        if seleccion:
            registro = self.resultados.get(seleccion)
            self.habilitar_campos()
            self.mi_nombre.set(registro[1])
            self.mi_duracion.set(registro[2])
            self.mi_genero.set(registro[3])
            self.mi_id_usuario.set(registro[4])
            self.mi_dni.set(registro[5])
            self.mi_direccion.set(registro[6])
            self.mi_celular.set(registro[7])
            self.mi_rol.set(registro[8])
            self.boton_guardar.config(command=lambda: self.actualizar_registro(registro[0]))

    def actualizar_registro(self, id_registro):
        datos = (self.mi_nombre.get(), self.mi_duracion.get(), self.mi_genero.get(), self.mi_id_usuario.get(), self.mi_dni.get(), self.mi_direccion.get(), self.mi_celular.get(), self.mi_rol.get(), id_registro)
        cursor.execute('''
            UPDATE usuarios
            SET nombre = ?, duracion = ?, genero = ?, id_usuario = ?, dni = ?, direccion = ?, celular = ?, rol = ?
            WHERE id = ?
        ''', datos)
        conn.commit()
        messagebox.showinfo('Actualizar', 'Registro actualizado con éxito')
        self.deshabilitar_campos()
        self.mostrar_datos()

    def eliminar_registro(self):
        seleccion = self.resultados.curselection()
        if seleccion:
            registro = self.resultados.get(seleccion)
            confirmacion = messagebox.askyesno('Confirmar', '¿Deseas eliminar este registro?')
            if confirmacion:
                cursor.execute('DELETE FROM usuarios WHERE id = ?', (registro[0],))
                conn.commit()
                messagebox.showinfo('Eliminar', 'Registro eliminado con éxito')
                self.mostrar_datos()

def iniciar_sesion():
    def verificar_credenciales():
        user_id = entry_user_id.get()
        password = entry_password.get()

        if user_id == USER_ID and password == PASSWORD:
            messagebox.showinfo('Acceso permitido', 'Usuario y contraseña correctos')
            ventana_login.destroy()
            root = tk.Tk()
            root.title('Ventana Principal')
            root.geometry('600x400')
            app = Frame(root=root)
            app.mainloop()
        else:
            messagebox.showerror('Acceso denegado', 'Usuario o contraseña incorrectos')

    ventana_login = tk.Tk()
    ventana_login.title('Inicio de Sesión')
    ventana_login.geometry('300x150')

    label_user_id = tk.Label(ventana_login, text='User ID:')
    label_user_id.pack(pady=5)
    entry_user_id = tk.Entry(ventana_login)
    entry_user_id.pack(pady=5)

    label_password = tk.Label(ventana_login, text='Password:')
    label_password.pack(pady=5)
    entry_password = tk.Entry(ventana_login, show='*')
    entry_password.pack(pady=5)

    boton_login = tk.Button(ventana_login, text='Login', command=verificar_credenciales)
    boton_login.pack(pady=5)

    ventana_login.mainloop()

if __name__ == '__main__':
    iniciar_sesion()
