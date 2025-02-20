from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def obtener_conexion():
    conn = sqlite3.connect('empresa.db')
    conn.row_factory = sqlite3.Row  # Esto nos permite acceder a las filas por nombre de columna
    return conn

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Página para agregar un proveedor
@app.route('/agregar_proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO proveedores (nombre, telefono, email, direccion)
        VALUES (?, ?, ?, ?)
        ''', (nombre, telefono, email, direccion))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('agregar_proveedor.html')

# Página para agregar un producto
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

# Página para ver los proveedores y los productos que ofrecen
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
    app.run(debug=True)
