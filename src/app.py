from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from form import RegisterStudentForm, RegisterGrades


import os
import conexion as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src' , 'templates')

app = Flask(__name__, static_folder='templates/assets')
app.secret_key = '1p1qswA@'




# --------- METODOS GENERALES


@app.route('/')
def login():
    return render_template('pages-login.html')

@app.route('/pages-login.html')
def login2():
    return render_template('pages-login.html')


@app.route('/index')
def index():
    return render_template('users-index.html')



@app.route('/pages-register.html')
def registra():
    """
    FALTA
    IMPLEMENTACIÓN DEL REGISTER
    """
    
    return render_template('pages-register.html')




@app.route('/login', methods=['POST'])
def log():

    """
    Metodo de inicio de sesión principal
    Ya sea usuario o alumno, se realizan las dos consultas y accedes al panel correspondiente
    Se generan sesiones para cada individuo correspondiente


    ***FALTA***:

    1. Verificar los campos de forma segura para evitar ataques SQL INJECTION
    2. OPCIONAL: Casilla recuerdame (COOKIES)

    """

    username = request.form['username']
    password = request.form['password']
    
    if username and password:
        cursor = db.database.cursor()
        sql_usuario = "SELECT NOMBRE, EMAIL, PASSWORD, USERNAME FROM USUARIOS WHERE USERNAME = %s"
        sql_alumno = "SELECT NOMBRE, APATERNO, AMATERNO, BOLETA, CORREO, CONTRASENA FROM ALUMNOS WHERE BOLETA = %s"
        
        cursor.execute(sql_usuario, (username,))
        stored_data_usuario = cursor.fetchone()

        cursor.execute(sql_alumno, (username,))
        stored_data_alumno = cursor.fetchone()

        if stored_data_usuario and stored_data_usuario[2] == password:
            # Si es un usuario gestor (en la tabla USUARIOS)
            session['logged_in'] = True
            session['username'] = username
            session['nombre'] = stored_data_usuario[0]
            session['correo'] = stored_data_usuario[1]
            return redirect(url_for('home'))
        elif stored_data_alumno and stored_data_alumno[5] == password:
            # Si es un alumno (en la tabla ALUMNOS)
            session['logged_in'] = True
            session['username'] = username
            session['nombre'] = stored_data_alumno[0]
            session['apellido_paterno'] = stored_data_alumno[1]
            session['apellido_materno'] = stored_data_alumno[2]
            session['correo'] = stored_data_alumno[4]
            return redirect(url_for('index'))
        else:
            # Si las credenciales son incorrectas o el usuario no se encuentra en ninguna tabla
            error_msg = 'Credenciales incorrectas. Inténtalo de nuevo.'
            return render_template('pages-login.html', error=error_msg)
    else:
        # Si no se proporcionaron datos de usuario o contraseña
        error_msg = 'Por favor, ingresa usuario y contraseña.'
        return render_template('pages-login.html', error=error_msg)



@app.route('/logout')
def logout():
    """
    Permite salir de la sesión actual por medio de icono SALIR
    """
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


#  ------------------------------ VENTANA PERFIL ---------

@app.route('/profile')
def profile():

    """
    Por medio de los datos de sesión, despliega la información del perfil en la pestaña Profile
    """

    alumno = {
        'Nombre': session.get('nombre'),
        'Apellido Paterno': session.get('apellido_paterno'),
        'Apellido Materno': session.get('apellido_materno'),
        'Correo': session.get('correo'),
        'Contraseña': session.get('contrasena')
        
    }
    
    return render_template('users-profile.html', alumno=alumno)

@app.route('/change_password', methods=['POST'])
def change_password():

    """
    Por terminar

    Este metodo permite cambiar la contraseña de los alumnos en su panel de 'Perfil'
    """

    if 'username' in session:  # Verifica que el usuario esté autenticado
        current_username = session['username']
        current_password = request.form['password']
        new_password = request.form['newpassword']
        reentered_password = request.form['renewpassword']

        if current_password and new_password and reentered_password:
            cursor = db.database.cursor()
            # Verificar la contraseña actual en la base de datos
            sql = "SELECT password FROM ALUMNOS WHERE USERNAME = %s"
            cursor.execute(sql, (current_username,))
            stored_password = cursor.fetchone()

            if stored_password and check_password_hash(stored_password[0], current_password):
                if new_password == reentered_password:
                    # Actualizar la contraseña en la base de datos
                    hashed_password = generate_password_hash(new_password)
                    update_sql = "UPDATE ALUMNOS SET PASSWORD = %s WHERE USERNAME = %s"
                    cursor.execute(update_sql, (hashed_password, current_username))
                    db.database.commit()
                    return "Contraseña actualizada exitosamente"
                else:
                    error_msg = "Las contraseñas nuevas no coinciden. Inténtalo de nuevo."
                    return "Las contraseñas nuevas no coinciden. Inténtalo de nuevo."
            else:
                return "La contraseña actual es incorrecta. Inténtalo de nuevo."

    # Si el usuario no está autenticado o faltan datos en el formulario
    return redirect(url_for('login'))  # Redirige al inicio de sesión o a donde sea apropiado



#  ----------------------- DEBUG

@app.route('/alumnos')
def mostrar_alumnos():

    """
    **SOLO PARA DEBUG**
    La ruta /alumnos muestra los registros de la db de la tabla ALUMNOS
    """

    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM ALUMNOS")
    usuarios = cursor.fetchall()
    print(usuarios)
    return render_template('usuarioss.html', usuarios=usuarios)

@app.route('/usuarios')
def mostrar_usuarios():
    """
    **SOLO PARA DEBUG**
    La ruta /usuarios muestra los registros de la db de la tabla USUARIOS 
    USUARIOS es el nombre de los gestores
    """
    cursor = db.database.cursor()
    cursor.execute("SELECT NOMBRE, EMAIL, PASSWORD, USERNAME FROM USUARIOS")
    usuarios = cursor.fetchall()

    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/addUsr',methods=['POST'])
def reg():
    """
    **SOLO PARA DEBUG**
    Permite insertar campos de USUARIOS

    """
    nombre = request.form['name']
    correo = request.form['email']
    username = request.form['username']
    contra = request.form['password']

    if nombre and correo and username and contra:
        cursor = db.database.cursor()
        sql = "INSERT INTO USUARIOS (EMAIL,NOMBRE,PASSWORD,USERNAME) VALUES (%s, %s, %s, %s)"
        data = (correo,nombre,contra,username)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('login'))


@app.route('/addAlumno',methods=['POST'])
def addAlumno():
    """
    **SOLO PARA DEBUG**
    Permite insertar campos de ALUMNOS

    """

    nombre = request.form['nombre']
    aPater = request.form['aPater']
    aMater = request.form['aMater']
    boleta = request.form['boleta']
    correo = request.form['correo']
    contra = request.form['contra']
    foto = request.form['foto']

    if nombre and aPater and aMater and boleta and correo and contra:
        cursor = db.database.cursor()
        sql = "INSERT INTO ALUMNOS (NOMBRE,APATERNO,AMATERNO,BOLETA,CORREO,CONTRASENA,FOTO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (nombre, aPater, aMater, boleta, correo, contra, foto)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))


#  --------------------------------------------- GESTION

@app.route("/register_students", methods=["GET", "POST"])
def register_students():
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form["nombre"]
        apellido_Paterno = request.form["aPater"]
        apellido_Materno = request.form["aMater"]
        boleta = request.form["boleta"]
        correo = request.form["correo"]
        password = request.form["contra"]
        foto = request.files["foto"]  # Aquí se obtiene el archivo de imagen

        try:
            cursor = db.database.cursor()
            sql = "INSERT INTO ALUMNOS (NOMBRE, APATERNO, AMATERNO, BOLETA, CORREO, CONTRASENA, FOTO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = (nombre, apellido_Paterno, apellido_Materno, boleta, correo, password, foto.filename)
            cursor.execute(sql, data)
            db.database.commit()

            # Guardar el archivo de imagen en tu sistema de archivos CAMBIA LA RUTA O APLICA EL METODO QUE HICISTE
            foto.save("/home/ed/Materias/Distribuidos/proyectofinal/distribuidos/fotos_perfil" + foto.filename)

            flash("Alumno registrado correctamente", "success")
            return redirect(url_for("register_students"))  # Redirigir a la página principal o a donde sea necesario

        except Exception as e:
            flash("Ocurrió un error al registrar al alumno: " + str(e), "error")

    return render_template("g-students-register.html")


@app.route("/grades", methods=["GET", "POST"])
def home():
    form = RegisterGrades()

    if form.validate_on_submit():
        boleta = request.form["boleta"]
        semestre = request.form["semestre"]
        materias = request.form["materias"]

        try:
            # De manera similar, aquí necesitas ejecutar tu lógica de inserción en la base de datos
            flash("Calificaciones registradas correctamente", "success")

        except Exception as e:
            flash("Ocurrió un error al registrar las calificaciones: " + str(e), "error")

    return render_template("g-students-grades.html", form=form)



# Funcion para guardar los archivos en la carpeta static
def upload_File(file, folder_Path):
    app.config["UPLOAD_FOLDER"] = folder_Path

    file.save(
        os.path.join(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(file.filename),
            )
        )
    )



if __name__ == '__main__':
    app.run(debug=True, port=4000)