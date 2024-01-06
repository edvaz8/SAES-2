from flask_wtf import FlaskForm
from wtforms import EmailField, FileField, IntegerField, SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileRequired, FileAllowed


# Clase para la creacion del formulario de registro de alumnos
class RegisterStudentForm(FlaskForm):
    # Declarando los campos del formulario con sus parametros de validacion
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=30)])
    apellido_Paterno = StringField("Apellido Paterno", validators=[DataRequired(), Length(max=30)])
    apellido_Materno = StringField("Apellido Materno", validators=[DataRequired(), Length(max=30)])
    boleta = StringField("Boleta", validators=[DataRequired(), Length(max=20)])
    correo = EmailField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Guardar Alumno")


# Clase para la creacion del formulario de registro de calificaiones
class RegisterGrades(FlaskForm):
    # Declarando los campos del formulario con sus parametros de validacion
    boleta = StringField("Boleta", validators=[DataRequired(), Length(max=20)])
    semestre = IntegerField("Semestre", validators=[DataRequired()])
    materias = SelectField("Materias", choices=[('Matematicas', 'Matematicas'), ('Historia', 'Historia'), ('Ciencias', 'Ciencias')])
    calificaciones_Excel = FileField('Calificaiones', validators=[FileAllowed(['xls', 'xlsx'], 'Excel files only!')])
    submit = SubmitField("Asignar Materia y Calificaciones")
