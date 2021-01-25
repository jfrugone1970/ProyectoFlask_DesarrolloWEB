from flask import Flask, flash, redirect, url_for, render_template, request
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'

# Conexion con la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyectoflask'

mysql = MySQL(app)

# Comntext processor

@app.context_processor
def date_now():
    return {
        'now': datetime.utcnow()
    }

# end points

@app.route('/')

def index():
    
    info = "Inicio"
    title = "Pagina de inicio de Proyecto Flask"
    edad = 50
    personas = ['Victor', 'Paco', 'Francisco', 'Raul', 'Andres', 'Paul']
    
    return render_template('index.html',
                            info=info,
                            title=title,
                            personas=personas,
                            edad=edad)

@app.route('/informacion')
@app.route('/informacion/<string:nombre>/<string:apellidos>')

def informacion(nombre=None, apellidos=None):
    
    texto = ""

    nombre = 'Lcdo. Jose Fernando'
    apellidos = 'Frugone Jaramillo'

    if nombre != None and apellidos != None:

        texto = f"""
                 <h1> Informacion </h1>
                 <p> Pagina de informacion </p>
                 <h3>Bienvenido, {nombre} {apellidos} </h3>  

                """ 

        return render_template('informacion.html',
                                texto=texto,
                                title="informacion")

    texto = f"""
               <h1> Informacion </h1>
               <p> Pagina de Informacion </p>
               <h3> Bienvenido, {nombre} {apellidos} </h3>
             """
   

    return render_template('informacion.html',
                            texto=texto,
                            title="Informacion")

@app.route('/contacto')
@app.route('/contacto/<string:redireccion>')

def contacto(redireccion = None):

    if redireccion != None:

        return redirect(url_for('lenguajes'))

    info = "Contacto"
    texto = "<h3> Pagina de Contacto </h3>"
    texto2 = "<h1> Aprendiendo Flask con Victor Robles"

    return render_template('contacto.html',
                            texto=texto,
                            texto2=texto2,
                            info=info) 
   

@app.route('/lenguajes')

def lenguajes():

    info = "Lenguajes"
    texto = "<h3> Pagina de Lenguajes </h3>"
    title = "<h2> Aprendiendo Flak con Victor Robles </h2>"

    return render_template('lenguajes.html', texto=texto, info=info, title=title) 

@app.route('/insertar_coche', methods=['GET', 'POST'])

def insertar_coche():

    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches(id, marca, modelo, precio, ciudad) VALUES(null, %s, %s, %s, %s)",(marca,modelo,precio,ciudad))
        cursor.connection.commit()

        flash('Has creado el coche correctamente!!!!')
        
        return redirect(url_for('index'))

    return render_template('crear_coche.html',title="Crear Coche")

@app.route('/crear_agenda', methods=['GET', 'POST'])

def crear_agenda():

    if request.method == 'POST':

        ## Pasa los valores por parametros

        apellido = request.form['apellidos']
        nombre = request.form['nombres']
        direccion = request.form['direccion']
        fono = request.form['telefono']
        pais = request.form['pais']
        ciudad = request.form['ciudad']
     
        cursor = mysql.connection.cursor()

        cursor.execute("INSERT INTO agenda(id,apellidos,nombres,direccion,telefono,pais,ciudad) VALUES(null, %s, %s, %s, %s, %s, %s)",(apellido,nombre,direccion,fono,pais,ciudad))
        cursor.connection.commit()

        flash("Has creado datos en la agenda correctamente...!!!!")

        return redirect(url_for('index'))

    return render_template('crea_agenda.html',title="Crear agenda")    



@app.route('/crea_articulo', methods=['GET', 'POST'])

def crea_articulo():

    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO articulos(id, marca, modelo, precio) VALUES(null, %s, %s, %s)", (marca, modelo, precio))
        cursor.connection.commit()

        flash('Has creado el articulo correctamente')

        return redirect(url_for('index'))

    return render_template('crear_articulo.html', title="Crear Articulo")    



@app.route('/coches')
def coches():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches")

    coches = cursor.fetchall()
    cursor.close()

    return render_template('coches.html', coches=coches, title="Listado de Coches")

@app.route('/agendas')
def agendas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM agenda")

    agendas = cursor.fetchall()
    cursor.close()

    return render_template('agendas.html', agendas=agendas, title="Listado de agenda")


@app.route('/lista_articulos')
def lista_articulos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM articulos")

    articulos = cursor.fetchall()
    cursor.close()

    return render_template('articulos.html', articulos=articulos, title="Listado de Articulos")


@app.route('/detalle_coches/<coche_id>')
def detalle_coches(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s", coche_id)

    coches = cursor.fetchall()
    cursor.close()

    return render_template('detalle.html', coches=coches, title="Detalle de Coche")

@app.route('/detalle_articulo/<articulo_id>')
def detalle_articulo(articulo_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM articulos WHERE id = %s", articulo_id)

    articulos = cursor.fetchall()
    cursor.close()

    return render_template('detalle_art.html', articulos=articulos, title="Detalle de  Articulos")

@app.route('/detalle_agenda/<agenda_id>')
def detalle_agenda(agenda_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM agenda WHERE id = %s", agenda_id)

    agendas = cursor.fetchall()
    cursor.close()

    return render_template('detalle_agenda.html', agendas=agendas, title="Detalle de Agendas")


@app.route('/borrar_coches/<coche_id>')
def borrar_coches(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM coches WHERE id = %s", coche_id)
    mysql.connection.commit()

    flash('El coche ha sido eliminado !!!')
    
    return redirect(url_for('index'))

@app.route('/borrar_articulo/<articulo_id>')
def borrar_articulo(articulo_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM articulos WHERE id = %s", articulo_id)
    mysql.connection.commit()

    flash('El articulo ha sido eliminado !!!')

    return redirect(url_for('index'))

@app.route('/borrar_agenda/<agenda_id>')
def borrar_agenda(agenda_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM agenda WHERE id = %s", agenda_id)
    mysql.connection.commit()

    flash('Has eliminado persona de agenda !!!')

    return redirect(url_for('index')) 


@app.route('/editar_coches/<coche_id>', methods=['GET', 'POST'])

def editar_coches(coche_id):

    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        cursor = mysql.connection.cursor()
        cursor.execute("""
               UPDATE coches
                SET marca = %s,
                    modelo = %s,
                    precio = %s,
                    ciudad = %s
                WHERE id = %s    

        """, (marca, modelo, precio, ciudad, coche_id))
        cursor.connection.commit()

        flash('Has editado el coche correctamente....!')

        edad = 50
        
        return redirect(url_for('index'))

    cursor2 = mysql.connection.cursor()
    cursor2.execute("SELECT * FROM coches WHERE id = %s", (coche_id))

    coches = cursor2.fetchall()

    edad = 50
    
    return render_template('crear_coche.html',
                            title='Crear coche',
                            info='Coches',
                            edad=edad,
                            coches=coches)

@app.route('/editar_agenda/<agenda_id>', methods=['GET', 'POST'])

def editar_agenda(agenda_id):

    if request.method == 'POST':

        apellidos = request.form['apellidos']
        nombres = request.form['nombres']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        pais = request.form['pais']
        ciudad = request.form['ciudad']

    
        cursor = mysql.connection.cursor()
        cursor.execute("""
               UPDATE agenda
                SET apellidos = %s,
                    nombres = %s,
                    direccion = %s,
                    telefono = %s,
                    pais = %s,
                    ciudad = %s
                WHERE id = %s    

        """, (apellidos,nombres,direccion,telefono,pais,ciudad,agenda_id))
        cursor.connection.commit()

        flash('Has editado la agenda correctamente....!')

        edad = 50
        
        return redirect(url_for('index'))

    cursor2 = mysql.connection.cursor()
    cursor2.execute("SELECT * FROM agenda WHERE id = %s", (agenda_id))

    agendas = cursor2.fetchall()

    edad = 50
    
    return render_template('crea_agenda.html',
                            title='Crear agendas',
                            info='Agendas',
                            edad=edad,
                            agendas=agendas)


@app.route('/editar_articulo/<articulo_id>', methods=['GET', 'POST'])

def editar_articulo(articulo_id):

    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']

        cursor = mysql.connection.cursor()
        cursor.execute("""
               UPDATE articulos
                SET marca = %s,
                    modelo = %s,
                    precio = %s
                WHERE id = %s    

        """, (marca, modelo, precio, articulo_id))
        cursor.connection.commit()

        flash('Has editado el articulo correctamente....!')

        edad = 50
        
        return redirect(url_for('index'))

    cursor2 = mysql.connection.cursor()
    cursor2.execute("SELECT * FROM articulos WHERE id = %s", (articulo_id))

    articulos = cursor2.fetchall()

    edad = 50
    
    return render_template('crear_articulo.html',
                            title='Crear Articulo',
                            info='Articulos',
                            edad=edad,
                            articulos=articulos)


   
    
@app.route('/coche_unico/<coche_id>')
def coche_unico(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s",coche_id)

    coches = cursor.fetchall()
    cursor.close()

    return render_template('crear_coche.html', coches=coches, title="Crear/Editar Coche")

    
if __name__ == '__main__':
    app.run(debug=True)