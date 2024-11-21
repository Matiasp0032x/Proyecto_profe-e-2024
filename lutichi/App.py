from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "lutichi"

# Función para obtener una conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lutichi'
    )

# Diccionario de usuarios 
usuarios_login = {
    "Daichi Uesugui": {"password": "daichino"},
    "Lujan Ramirez": {"password": "lujijaja"},
    "Matias Pereira": {"password": "elmati777"}
}

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Obtener las categorías (géneros) disponibles
    cursor.execute("SELECT DISTINCT genero FROM producto")
    categorias = cursor.fetchall()

    # Obtener 5 libros por cada categoría
    libros_por_categoria = {}
    for categoria in categorias:
        cursor.execute("""
            SELECT * FROM producto 
            WHERE genero = %s
            LIMIT 5
        """, (categoria[0],))
        libros_por_categoria[categoria[0]] = cursor.fetchall()

    cursor.close()
    connection.close()
    libro1 = 'aventura1'
    libro2 = 'misterio1'
    libro3 = 'misterio2'
    libro4 = 'realismo_magico1'
    libro5 = 'distopia1'
    libro6 = 'ficcion2'
    lutichi1 = 'lutichi1'
    return render_template('index.html', categorias=categorias, libros_por_categoria=libros_por_categoria, libro1=libro1, libro2=libro2, libro3=libro3, libro4=libro4, libro5=libro5, libro6=libro6, lutichi1=lutichi1)

@app.route('/usuarios')
def usuarios():
    # Ruta principal para mostrar todos los clientes
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cliente')
        clientes = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Error al obtener los clientes: {e}", "danger")
        clientes = []
    finally:
        cursor.close()
        db.close()
        lutichi1 = 'lutichi1'
    return render_template('usuarios.html', clientes=clientes, lutichi1=lutichi1)

@app.route('/personal')
def personal():
    # Ruta principal para mostrar todos los vendedores
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM vendedor')
        vendedor = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Error al obtener los vendedores: {e}", "danger")
        vendedor = []
    finally:
        cursor.close()
        db.close()
        lutichi1 = 'lutichi1'
    return render_template('personal.html', vendedor=vendedor, lutichi1=lutichi1)

@app.route('/main', methods=['GET', 'POST'])
def main2():
    usuario = session.get('usuario', None)
    lutichi1 = 'lutichi1'
    return render_template('main.html',usuario=usuario, lutichi1=lutichi1)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('u')
        password = request.form.get('p')

        # Verificar las credenciales (ejemplo simple)
        if username in usuarios_login and usuarios_login[username]['password'] == password:
            session['usuario'] = username
            flash("Sesión iniciada correctamente", "success")
            print(f"Sesión iniciada para: {username}")  # Verificar en la consola
            return redirect('/main')
        else:
            flash("Credenciales incorrectas", "danger")
    lutichi1 = 'lutichi1'
    return render_template('login.html', lutichi1=lutichi1)

@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Elimina al usuario de la sesión
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('index'))  # Redirige a la página de inicio


@app.route('/cliente', methods=['POST'])
def agregar_cliente():
    # Ruta para agregar un nuevo cliente
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')

        if not cedula or not nombre or not email or not telefono:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('usuarios'))

        try:
            db = get_db_connection()
            cursor = db.cursor()
            query = "INSERT INTO cliente (cedula, nombre, email, telefono) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (cedula, nombre, email, telefono))
            db.commit()
            flash('Cliente agregado exitosamente', 'success')
        except mysql.connector.Error as e:
            flash(f"Error al agregar el cliente: {e}", "danger")
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('usuarios'))

@app.route('/editar_cliente', methods=['POST'])
def editar_cliente():
    # Ruta para editar un cliente existente
    id_cliente = request.form.get('id_cliente')
    cedula = request.form.get('cedula')
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    telefono = request.form.get('telefono')

    if not id_cliente or not cedula or not nombre or not email or not telefono:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for('usuarios'))

    try:
        db = get_db_connection()
        cursor = db.cursor()
        query = """UPDATE cliente
                    SET cedula = %s, nombre = %s, email = %s, telefono = %s
                    WHERE id_cliente = %s"""
        cursor.execute(query, (cedula, nombre, email, telefono, id_cliente))
        db.commit()
        flash('Cliente actualizado exitosamente', 'success')
    except mysql.connector.Error as e:
        flash(f"Error al actualizar el cliente: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('usuarios'))

@app.route('/eliminar/<int:id_cliente>')
def eliminar_cliente(id_cliente):
    # Ruta para eliminar un cliente por su ID
    try:
        db = get_db_connection()
        cursor = db.cursor()
        query = "DELETE FROM cliente WHERE id_cliente = %s"
        cursor.execute(query, (id_cliente,))
        db.commit()
        flash('Cliente eliminado exitosamente', 'danger')
    except mysql.connector.Error as e:
        flash(f"Error al eliminar el cliente: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('usuarios'))

#Seccion del personal
@app.route('/personales', methods=['POST'])
def agregar_personal():
    # Ruta para agregar un nuevo cliente
    if request.method == 'POST':
        nombre = request.form.get('nombre') 
        apellido = request.form.get('apellido')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')

        if not apellido or not nombre or not direccion or not telefono:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('personal'))

        try:
            db = get_db_connection()
            cursor = db.cursor()
            query = "INSERT INTO vendedor (nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, apellido, direccion, telefono))
            db.commit()
            flash('Personal agregado exitosamente', 'success')
        except mysql.connector.Error as e:
            flash(f"Error al agregar a el Personal: {e}", "danger")
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('personal'))

@app.route('/editar_personal', methods=['POST'])
def editar_personal():
    # Ruta para editar un vendedor existente
    id_vendedor = request.form.get('id_vendedor')
    nombre = request.form.get('nombre') 
    apellido = request.form.get('apellido')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')

    if not id_vendedor or not apellido or not nombre or not direccion or not telefono:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for('personal'))

    try:
        db = get_db_connection()
        cursor = db.cursor()
        query = """UPDATE vendedor
                    SET nombre = %s, apellido = %s, direccion = %s, telefono = %s
                    WHERE id_vendedor = %s"""
        cursor.execute(query, (nombre, apellido, direccion, telefono, id_vendedor))
        db.commit()
        flash('Personal actualizado exitosamente', 'success')
    except mysql.connector.Error as e:
        flash(f"Error al actualizar a el Personal: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('personal'))


@app.route('/eliminar/<int:id_vendedor>')
def eliminar_vendedor(id_vendedor):
    # Ruta para eliminar un personal por su ID
    try:
        db = get_db_connection()
        cursor = db.cursor()
        query = "DELETE FROM vendedor WHERE id_vendedor = %s"
        cursor.execute(query, (id_vendedor,))
        db.commit()
        flash('Personal eliminado exitosamente', 'danger')
    except mysql.connector.Error as e:
        flash(f"Error al eliminar a el Personal: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('personal'))

@app.route('/inventario')
def inventario():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM producto')
        productos = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Error al obtener el inventario: {e}", "danger")
        productos = []
    finally:
        cursor.close()
        db.close()
        lutichi1 = 'lutichi1'
    return render_template('inventario.html', productos=productos, lutichi1=lutichi1)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        autor = request.form.get('autor')
        genero = request.form.get('genero')
        precio = request.form.get('precio')
        cantidad = request.form.get('cantidad')
        disponibilidad = request.form.get('disponibilidad')
        descripcion = request.form.get('descripcion')
        imagen_url = request.form.get('imagen_url')

        if not nombre or not autor or not genero or not cantidad or not disponibilidad or not precio or not descripcion or not imagen_url:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('inventario'))

        try:
            db = get_db_connection()
            cursor = db.cursor()
            query = """INSERT INTO producto (nombre, autor, genero, precio, cantidad, disponibilidad, descripcion, imagen_url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (nombre, autor, genero, precio, cantidad, disponibilidad, descripcion, imagen_url))
            db.commit()
            flash('Producto agregado exitosamente', 'success')
        except mysql.connector.Error as e:
            flash(f"Error al agregar el producto: {e}", "danger")
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('inventario'))

@app.route('/editar_producto', methods=['POST'])
def editar_producto():
    id_producto = request.form.get('id_producto')
    nombre = request.form.get('nombre')
    autor = request.form.get('autor')
    genero = request.form.get('genero')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    disponibilidad = request.form.get('disponibilidad')
    descripcion = request.form.get('descripcion')
    imagen_url = request.form.get('imagen_url')

    if not id_producto or not nombre or not autor or not genero or not precio or not cantidad or not disponibilidad or not descripcion or not imagen_url:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for('inventario'))

    try:
        db = get_db_connection()
        cursor = db.cursor()
        query = """UPDATE producto
                    SET nombre = %s, autor = %s, genero = %s, precio = %s, cantidad = %s, disponibilidad = %s, descripcion = %s, imagen_url = %s
                    WHERE id_producto = %s"""
        cursor.execute(query, (nombre, autor, genero, precio, cantidad, disponibilidad, descripcion, imagen_url, id_producto))
        db.commit()
        flash('Producto actualizado exitosamente', 'success')
    except mysql.connector.Error as e:
        flash(f"Error al actualizar el producto: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('inventario'))

@app.route('/eliminar_producto/<int:id_producto>')
def eliminar_producto(id_producto):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        query = "DELETE FROM producto WHERE id_producto = %s"
        cursor.execute(query, (id_producto,))
        db.commit()
        flash('Producto eliminado exitosamente', 'danger')
    except mysql.connector.Error as e:
        flash(f"Error al eliminar el producto: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('inventario'))

@app.route('/factura')
def facturas():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Consulta para listar facturas
        query = """SELECT f.id_factura, c.nombre AS cliente, v.nombre AS vendedor, 
                            p.nombre AS producto, f.cantidad, 
                            (f.cantidad * p.precio) AS precio_total
                   FROM factura f
                   INNER JOIN cliente c ON f.id_cliente = c.id_cliente
                   INNER JOIN vendedor v ON f.id_vendedor = v.id_vendedor
                   INNER JOIN producto p ON f.id_producto = p.id_producto ORDER BY f.id_factura ASC"""
        cursor.execute(query)
        facturas = cursor.fetchall()
        
        # Consultas auxiliares para los formularios
        cursor.execute("SELECT id_cliente, nombre FROM cliente")
        clientes = cursor.fetchall()

        cursor.execute("SELECT id_vendedor, nombre FROM vendedor")
        vendedores = cursor.fetchall()

        cursor.execute("SELECT id_producto, nombre FROM producto")
        productos = cursor.fetchall()

        lutichi1 = 'lutichi1'
        return render_template('facturas.html', facturas=facturas, clientes=clientes, vendedores=vendedores, productos=productos, lutichi1=lutichi1)
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        db.close()

@app.route('/crear_factura', methods=['POST'])
def crear_factura():
    id_cliente = request.form.get('cliente')
    id_vendedor = request.form.get('vendedor')
    id_producto = request.form.get('id_producto')
    cantidad = request.form.get('cantidad')

    if not cantidad:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for('facturas'))

    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            flash("La cantidad debe ser mayor a 0.", "danger")
            return redirect(url_for('facturas'))

        db = get_db_connection()
        cursor = db.cursor()

        # Obtener información del producto
        cursor.execute("SELECT precio, cantidad FROM producto WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        if not producto:
            flash("El producto no existe.", "danger")
            return redirect(url_for('facturas'))

        precio, stock_actual = producto
        if stock_actual < cantidad:
            flash("No hay suficiente stock disponible.", "danger")
            return redirect(url_for('facturas'))

        # Calcular precio total y crear factura
        precio_total = precio * cantidad
        cursor.execute(
            """INSERT INTO factura (id_cliente, id_vendedor, id_producto, cantidad, preciototal)
                VALUES (%s, %s, %s, %s, %s)""",
            (id_cliente, id_vendedor, id_producto, cantidad, precio_total)
        )

        # Actualizar stock del producto
        cursor.execute(
            "UPDATE producto SET cantidad = cantidad - %s WHERE id_producto = %s",
            (cantidad, id_producto)
        )

        db.commit()
        flash("Factura creada exitosamente.", "success")
    except ValueError:
        flash("La cantidad debe ser un número válido.", "danger")
    except mysql.connector.Error as e:
        db.rollback()
        flash(f"Error al crear la factura: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('facturas'))

@app.route('/buscar_categoria', methods=['GET'])
def buscar_categoria():
    categoria = request.args.get('categoria', '')
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)  # Usar `dictionary=True` para obtener resultados como diccionarios.
        query = """
            SELECT * 
            FROM producto 
            WHERE LOWER(genero) = LOWER(%s)
        """
        cursor.execute(query, (categoria,))
        libros = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f"Error al buscar libros por categoría: {e}", "danger")
        libros = []
    finally:
        cursor.close()
        db.close()
        lutichi1 = 'lutichi1'
    return render_template('categoria.html', libros=libros, categoria=categoria, lutichi1=lutichi1)

if __name__ == '__main__':
    # Iniciar la aplicación Flask
    app.run(debug=True)