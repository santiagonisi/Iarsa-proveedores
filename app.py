from flask import Flask, render_template, request, redirect, url_for # type: ignore
import sqlite3

app = Flask(__name__)

#conectar a la base de datos
def obtener_conexion():
    conn = sqlite3.connect('empresa.db')
    conn.row_factory = sqlite3.Row  #acceder a las filas por nombre de columna
    return conn

#Página principal
@app.route('/')
def index():
    return render_template('index.html')

#agregar un proveedor
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
        INSERT INTO proveedores_productos (proveedor_id, producto_id, precio)
        VALUES (?, ?, ?)
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

#ver los proveedores y los productos de cada uno
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
