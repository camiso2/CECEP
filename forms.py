# from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SelectField, HiddenField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired,EqualTo


class FormLogin(FlaskForm):
    password =  PasswordField('password',
    [
    validators.Required( message='La contraseña es requerida !'),
    validators.length(min=4, max=80, message='Ingrese una contraseña valida !')
    ]
    )
    email = EmailField('Correo electrónico',
    [
    validators.Required( message='El Email es requerido !'),
    validators.length(min=6, max=80, message='Ingrese un Email valido !')
    ]
    )

class FormRegister(FlaskForm):
    institucion = TextField('Nombre institución',
    [
    validators.Required( message='La Institución es requerida !'),
    validators.length(min=2, max=60, message='Ingrese Nombre institución valido !')
    ]
    )

    representante = TextField('Nombre del representante',
    [
    validators.Required( message='El Nombre del representante es requerido !'),
    validators.length(min=2, max=60, message='Ingrese nombre del representante valido !')
    ]
    )
    email = EmailField('Correo electrónico',
    [
    validators.Required( message='El e-mail es requerido !'),
    validators.length(min=6, max=80, message='Ingrese un e-mail valido !')
    ]
    )
    departamento = TextField('Departamento',
    [
    validators.Required( message='El departamento es requerido !'),
    validators.length(min=6, max=25, message='Ingrese un departamento valido !')
    ]
    )
    telefono = IntegerField('Teléfono',
    [
    validators.Required( message='El telefono es requerido !'),
    #validators.length(min=6, max=25, message='Ingrese un departamento valido !')
    ]
    )

    ciudad = TextField('Ciudad',
    [
    validators.Required( message='La Ciudad es requerida !'),
    validators.length(min=6, max=25, message='Ingrese una ciudad valida !')
    ]
    )
    direccion = TextField('Direccion',
    [
    validators.Required( message='La direccion es requerida !'),
    validators.length(min=6, max=25, message='Ingrese una direccion valida !')
    ]
    ) 
    colegio = SelectField('Colegio', validators=[DataRequired()],choices=[('', 'seleccione'),('Oficial', 'Oficial'), ('privado', 'privado'), ('semiprivado', 'semi-Privado')  ])
    alumnos = SelectField('Alumnos', validators=[DataRequired()],choices=[('', 'seleccione'),('femenino', 'Femenino'), ('masculino', 'Masculino'), ('mixto', 'Mixto')  ])


    password =  PasswordField('password',
    [
    validators.Required( message='La contraseña es requerida !'),
    validators.length(min=4, max=80, message='Ingrese una contraseña valida !')
    ]
    )
    confirmPassword = PasswordField('Confirmar contraseña:',validators=[DataRequired(),EqualTo('password','Confirmación de contraseña invalida !')])


class FormRegisterEdit(FlaskForm):
    institucion = TextField('Nombre institución',
    [
    validators.Required( message='La Institución es requerida !'),
    validators.length(min=2, max=60, message='Ingrese Nombre institución valido !')
    ]
    )

    representante = TextField('Nombre del representante',
    [
    validators.Required( message='El Nombre del representante es requerido !'),
    validators.length(min=2, max=60, message='Ingrese nombre del representante valido !')
    ]
    )
    email = EmailField('Correo electrónico',
    [
    validators.Required( message='El e-mail es requerido !'),
    validators.length(min=6, max=80, message='Ingrese un e-mail valido !')
    ]
    )
    departamento = TextField('Departamento',
    [
    validators.Required( message='El departamento es requerido !'),
    validators.length(min=6, max=25, message='Ingrese un departamento valido !')
    ]
    )
    telefono = IntegerField('Teléfono',
    [
    validators.Required( message='El telefono es requerido !'),
    #validators.length(min=6, max=25, message='Ingrese un departamento valido !')
    ]
    )

    ciudad = TextField('Ciudad',
    [
    validators.Required( message='La Ciudad es requerida !'),
    validators.length(min=6, max=25, message='Ingrese una ciudad valida !')
    ]
    )
    direccion = TextField('Direccion',
    [
    validators.Required( message='La direccion es requerida !'),
    validators.length(min=6, max=25, message='Ingrese una direccion valida !')
    ]
    ) 
    colegio = SelectField('Colegio', validators=[],choices=[('', 'seleccione'),('Oficial', 'oficial'), ('privado', 'privado'), ('semiprivado', 'semi-Privado')  ])
    alumnos = SelectField('Alumnos', validators=[],choices=[('', 'seleccione'),('femenino', 'Femenino'), ('masculino', 'Masculino'), ('mixto', 'Mixto')  ])

class FormLoginEdit(FlaskForm):

    #updateRegister = HiddenField()

    CurrentPassword = PasswordField('Password actual',
    [
    validators.Required( message='La contraseña actual es requerida !'),
    validators.length(min=4, max=80, message='Ingrese la contraseña Aactual !')
    ]
    )
    password =  PasswordField('password',
    [
    validators.Required( message='La contraseña es requerida !'),
    validators.length(min=4, max=80, message='Ingrese una contraseña valida !')
    ]
    )
    confirmPassword = PasswordField('Confirmar contraseña:',validators=[DataRequired(),EqualTo('password','Confirmación de contraseña invalida !')])
   

    
    



    
 






    

