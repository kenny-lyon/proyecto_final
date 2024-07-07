import sqlite3

def create_tables():
    connection = sqlite3.connect('biblioteca.db')
    cursor = connection.cursor()

    # Crear tabla autores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS autores (
        idautor INTEGER PRIMARY KEY,
        NOMBRES TEXT NOT NULL,
        APELLIDOS TEXT NOT NULL,
        DNI TEXT NOT NULL,
        MODALIDAD TEXT NOT NULL,
        AUTORESCOL TEXT NOT NULL
    )
    ''')

    # Crear tabla categorias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        idcategoria INTEGER PRIMARY KEY,
        NOMBRE_CATEGORIA TEXT NOT NULL,
        UBICACION TEXT NOT NULL
    )
    ''')
    
    # Crear tabla libros
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS libros (
        idlibro INTEGER PRIMARY KEY,
        TITULO TEXT NOT NULL,
        AUTORES TEXT NOT NULL,
        EDICION TEXT NOT NULL,
        DESCRIPCION TEXT NOT NULL,
        AÑO TEXT NOT NULL,
        NUMEROPAGINAS INTEGER NOT NULL,
        CATEGORIA_IDCATEGORIA INTEGER,
        FOREIGN KEY (CATEGORIA_IDCATEGORIA) REFERENCES categorias(idcategoria)
    )
    ''')
    
    # Crear tabla libros_autores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS libros_autores (
        idlibro INTEGER,
        idautor INTEGER,
        PRIMARY KEY (idlibro, idautor),
        FOREIGN KEY (idlibro) REFERENCES libros(idlibro),
        FOREIGN KEY (idautor) REFERENCES autores(idautor)
    )
    ''')

    # Crear tabla prestamos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prestamos (
        idprestamo INTEGER PRIMARY KEY,
        idlibro INTEGER,
        idusuario INTEGER,
        fecha_prestamo TEXT NOT NULL,
        fecha_devolucion TEXT,
        FOREIGN KEY (idlibro) REFERENCES libros(idlibro),
        FOREIGN KEY (idusuario) REFERENCES usuarios(idusuario)
    )
    ''')

   

    # Crear tabla usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        idusuario INTEGER PRIMARY KEY,
        DNI TEXT NOT NULL,
        NOMBRES TEXT NOT NULL,
        APELLIDOS TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        DIRECCION TEXT NOT NULL,
        CELULAR TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Tablas creadas exitosamente.")
