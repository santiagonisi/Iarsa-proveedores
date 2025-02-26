from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#connect to the database
def obtener_conexion():
    conn = sqlite3.connect('empresa.db')
    conn.row_factory = sqlite3.Row  # access rows by column name
    return conn

#create the table centros_costos if it does not exist
def crear_tabla_centros_costos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS centros_costos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        departamento TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

#create the table centros_costos when the application starts
crear_tabla_centros_costos()

# Create the table proveedores if it does not exist
def crear_tabla_proveedores():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        razonsocial TEXT NOT NULL,
        contacto TEXT NOT NULL,
        cuit TEXT NOT NULL,
        rubro TEXT NOT NULL,
        ubicacion TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Create the table productos if it does not exist
def crear_tabla_productos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        cantidad INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

#create the tables proveedores and productos at application startup
def crear_tabla_proveedores_productos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores_productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proveedor_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        precio REAL,
        fecha TEXT,
        FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')
    conn.commit()
    conn.close()

# Create all necessary tables when the application starts
crear_tabla_proveedores()
crear_tabla_productos()
crear_tabla_proveedores_productos()


#Página principal
@app.route('/')
def index():
    return render_template('index.html')

#add a provider
@app.route('/agregar_proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        razonsocial = request.form['razonsocial']
        contacto = request.form['contacto']
        cuit = request.form['cuit']
        rubro = request.form['rubro']
        ubicacion = request.form['ubicacion']
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO proveedores (nombre, razonsocial, contacto, cuit, rubro, ubicacion)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, razonsocial, contacto, cuit, rubro, ubicacion))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('agregar_proveedor.html')

#agregar una cotizacion
@app.route('/agregar_cotizacion', methods=['GET', 'POST'])
def agregar_cotizacion():
    if request.method == 'POST':
        proveedor_id = request.form['proveedor_id']
        producto_id = request.form['producto_id']
        precio = request.form['precio']
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO proveedores_productos (proveedor_id, producto_id, precio, fecha)
        VALUES (?, ?, ?, NULL)
        ''', (proveedor_id, producto_id, precio))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores')
    proveedores = cursor.fetchall()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()

    return render_template('agregar_cotizacion.html', proveedores=proveedores, productos=productos)

#add a budget date
@app.route('/agregar_fecha', methods=['GET', 'POST'])
def agregar_fecha():
    if request.method == 'POST':
        proveedor_id = request.form['proveedor_id']
        producto_id = request.form['producto_id']
        fecha = request.form['fecha']
#add a quotation
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE proveedores_productos
        SET fecha = ?
        WHERE proveedor_id = ? AND producto_id = ?
        ''', (fecha, proveedor_id, producto_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores')
    proveedores = cursor.fetchall()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()

    return render_template('agregar_fecha.html', proveedores=proveedores, productos=productos)

# Add a cost center
@app.route('/agregar_centro_costos', methods=['GET', 'POST'])
def agregar_centro_costos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        departamento = request.form['departamento']
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO centros_costos (nombre, departamento)
        VALUES (?, ?)
        ''', (nombre, departamento))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('agregar_centro_costos.html')

#view cost center
@app.route('/centros_costos')
def centros_costos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM centros_costos')
    centros_costos = cursor.fetchall()
    conn.close()

    return render_template('centros_costos.html', centros_costos=centros_costos)
#add a product
#agregar un producto
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO productos (nombre, categoria, cantidad)
        VALUES (?, ?, ?)
        ''', (nombre, categoria, cantidad))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('agregar_producto.html')

#view providers and their products
@app.route('/proveedores')
def proveedores():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT p.nombre, pr.nombre AS producto, pp.precio
    FROM proveedores p
    JOIN proveedores_productos pp ON p.id = pp.proveedor_id
    JOIN productos pr ON pr.id = pp.producto_id
    ''')
    proveedores = cursor.fetchall()
    conn.close()

    return render_template('proveedores.html', proveedores=proveedores)

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
