import sqlite3

def crear_base_de_datos():
    """
    Crea la base de datos 'empresa.db' con las tablas 'proveedores', 'productos' y 'proveedores_productos'.
    """
    with sqlite3.connect('empresa.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                direccion TEXT
            )
''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria TEXT,
            cantidad INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores_productos (
            proveedor_id INTEGER,
            producto_id INTEGER,
            precio REAL,
            FOREIGN KEY(proveedor_id) REFERENCES proveedores(id),
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
    ''')

    conn.commit()
if __name__ == "__main__":
    # Ejecutamos la creación de la base de datos
    crear_base_de_datos()

