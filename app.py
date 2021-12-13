from logging import debug
from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash,g
from flask_wtf import CsrfProtect
from config import DevelopentConfig
from config import Alpha
from models import db
from models import User
from models import File
from flask import send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from collections import defaultdict
import collections, numpy
# robert
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler

import forms
import json


app= Flask(__name__)
app.config.from_object(DevelopentConfig)
#no permitir ataques csrf
#app.secret_key='my_secret_key'
csrf = CsrfProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
#decorador
@app.before_request
def before_request():
    url="->"

#decorador
@app.after_request
def before_request(response):
   # print("3")
    return response

@app.route("/logout")
def logout():
    if 'email' in session :
        session.pop('email')
    return redirect(url_for('login'))

@app.route("/welcome",)
def welcome():
    if 'email' not in session:
        return redirect(url_for('login'))
    dataUser = User.get_by_email(session['email'])
    
    count = File.get_by_count(dataUser.id)
    count_delete = File.get_by_count_delete(dataUser.id)
    if count<1 :
        count = 0
        count_delete = 0

    return render_template('/welcome.html',
    dataUser = dataUser,
    count=count, 
    count_delete=count_delete,
    tgg = totalGeneralGenero(dataUser.id),
    tge = totalGeneralEstudiantes(dataUser.id),
    tgc = estadoCivilGeneral(dataUser.id),
    desert = desertoresGeneral(dataUser.id),
    ps = pruebasSaberGeneral(dataUser.id),
    pb = padresBachilleresGeneral(dataUser.id),
    )
    #return render_template('/welcome.html',dataUser = dataUser )

 

@app.route("/evaluation",methods=['GET', 'POST'])
def evaluation():
    if 'email' not in session:
        return redirect(url_for('login'))
    dataUser = User.get_by_email(session['email'])
    if request.method == 'POST':
        id_file=request.form['id_file']
        file_first=File.get_by_file(id_file)
        # print(f"file_first::{file_first.archivo}")
        doc = 'upload/{}'.format(file_first.archivo)
        dataEXCEL = pd.read_excel(doc, sheet_name='dataset')
        # print(f"::datos del excel subido->>>>{dataEXCEL}")


        # Se crea la Matrix de las variables X (features) y de la función y (Target)
        xn = dataEXCEL.iloc[:,0:8].values
        yn = dataEXCEL.iloc[:,8].values
        print(f"iloc xn---->{xn.shape}")
        print(f"iloc yn---->{yn.shape}")
        print(f"::datos del excel subido->>>>{dataEXCEL}")
        # dataEXCEL.head()

        labelencoder_xn = LabelEncoder()
        xn[:,0] = labelencoder_xn.fit_transform(xn[:,0])
        xn[:,2] = labelencoder_xn.fit_transform(xn[:,2])
        xn[:,3] = labelencoder_xn.fit_transform(xn[:,3])
        xn[:,5] = labelencoder_xn.fit_transform(xn[:,5])
        labelencoder_yn = LabelEncoder()
        yn = labelencoder_xn.fit_transform(yn)

        print("CODIFICANCO DATOS CATEGORICOS")
        print("variables categoricas a ordinales !!")
        print(f"xn[0,:]--->{xn[0,:]}")
        print(f"yn[0]--->{yn[0]}")
        print(xn.shape)

        print("creando variables dummy !!")
        ct = ColumnTransformer([('one_hot_encoder', OneHotEncoder(categories='auto'), [0,3,5])],remainder='passthrough')
        xn = np.array(ct.fit_transform(xn))
        print(f"xn[0,:]--->{xn[0,:]}")
        print(f"yn[0]--->{yn[0]}")
        print(xn.shape)
        print("CODIFICANCO DATOS CATEGORICOS")
        scaler = MinMaxScaler()
        xn = scaler.fit_transform(xn[:, :14])
        print(f"xn[0,:]--->{xn[0,:]}")
        print(f"yn--->{yn}")
        # print(f"::datos del excel subido->>>>{dataEXCEL}")
        total_estudiantes=len(dataEXCEL.axes[0])
        print(f"::totl de columnas->>>>{total_estudiantes}")
        dataEvaluation = np.concatenate((dataEXCEL,yn[:,None]),axis=1)

        alenyn = np.array(yn)
        _instanceyn = list(alenyn)
        count_1yn = _instanceyn.count(1)
        count_0yn = _instanceyn.count(0)

        #contando columnas a partir de dataExcel
        dat_g = dataEXCEL['Genero'].value_counts()
        dat_d = dataEXCEL['deser++++tores'].value_counts()
        dat_pb = dataEXCEL['Padre Bachiller'].value_counts()
        dat_ps = dataEXCEL['Pruebas Saber'].value_counts()
        dat_ec = dataEXCEL['Estado civil'].value_counts()
        count = File.get_by_count(dataUser.id)
        count_delete = File.get_by_count_delete(dataUser.id)
        return render_template('/evaluation.html',
        dataUser = dataUser,
        count=count,
        count_delete=count_delete,
        excel_new = dataEvaluation,
        total_estudiantes=total_estudiantes,
        c0 = count_0yn,
        c1=count_1yn,
        genero = dat_g,
        desertores = dat_d,
        pb = dat_pb,
        ps = dat_ps,
        ec = dat_ec,
        tgg = totalGeneralGenero(dataUser.id),
        tge = totalGeneralEstudiantes(dataUser.id),
        )


def totalGeneralGenero(dataUser):
  
    dat_general_genero = 0
    all_excel = File.get_by_all_files_state(dataUser)
    for files_db in all_excel:
        doc = 'upload/{}'.format(files_db.archivo)
        dataEXCEL_all = pd.read_excel(doc, sheet_name='dataset')
        dat_general_genero = dataEXCEL_all['Genero'].value_counts()+dat_general_genero
    return dat_general_genero



def totalGeneralEstudiantes(dataUser):
    total_general = 0
    all_excel = File.get_by_all_files_state(dataUser)
    for files_db in all_excel:
        doc = 'upload/{}'.format(files_db.archivo)
        dataEXCEL_all = pd.read_excel(doc, sheet_name='dataset')
        total_general=len(dataEXCEL_all.axes[0])+total_general
    return total_general
def padresBachilleresGeneral(dataUser):
    dat_general = 0
    all_excel = File.get_by_all_files_state(dataUser)
    for files_db in all_excel:
        doc = 'upload/{}'.format(files_db.archivo)
        dataEXCEL_all = pd.read_excel(doc, sheet_name='dataset')
        dat_general = dataEXCEL_all['Padre Bachiller'].value_counts()+dat_general
    return dat_general    
def pruebasSaberGeneral(dataUser):
    dat_general = 0
    all_excel = File.get_by_all_files_state(dataUser)
    for files_db in all_excel:
        doc = 'upload/{}'.format(files_db.archivo)
        dataEXCEL_all = pd.read_excel(doc, sheet_name='dataset')
        dat_general = dataEXCEL_all['Pruebas Saber'].value_counts()+dat_general
    return dat_general

def desertoresGeneral(dataUser):
    dat_general = 0
    all_excel = File.get_by_all_files_state(dataUser)
    for files_db in all_excel:
        doc = 'upload/{}'.format(files_db.archivo)
        dataEXCEL_all = pd.read_excel(doc, sheet_name='dataset')
        dat_general = dataEXCEL_all['
        '].value_counts()+dat_general
    return dat_general  

def estadoCivilGeneral(dataUser):
    dat_general = 0
    all_excel = File.get_by_all_files_state(dataUser)
    for files_db in all_excel:
        doc = 'upload/{}'.format(files_db.archivo)
        dataEXCEL_all = pd.read_excel(doc, sheet_name='dataset')
        dat_general = dataEXCEL_all['Estado civil'].value_counts()+dat_general
    return dat_general   

@app.route("/",methods=['GET', 'POST'])
def login():

    login_form = forms.FormLogin(request.form)
    if request.method == 'POST' and login_form.validate():
        password=login_form.password.data
        email=login_form.email.data
        # password_verify = User.get_by_password(password)
        user = User.get_by_email(email)
        encrypNewPass = "".join([(str(ord(x)-96) if x.isalpha() else x) for x in list(password)])
        encrypNewPass = int(password)
        #encryptando contraseña ingresada por uausuario
        encryPassword= User._encryptSuperHard(Alpha.alpha().lower(),encrypNewPass)
        print(f"login que es ;::{encryPassword}")


        if (user is not None and encryPassword == user.password ):
            session['email'] = user.email
            return redirect(url_for('welcome'))
        else:
            error_message= 'Usuario o password no validos!'
            flash(error_message)
            return redirect('/')
    logout()
    return render_template('login.html', form = login_form )



@app.route("/edit-register",methods=['GET', 'POST'])
def edit_register():
    #validando que el usuario tenga una sesión abierta
    if 'email' not in session:
        return redirect(url_for('login'))
    dataUser = User.get_by_email(session['email'])
    if request.method == 'POST' and request.form['updateRegister'] == "updateRegister":
        #validación de form
        institucion=request.form['institucion']
        representante=request.form['representante']
        email=request.form['email']
        departamento=request.form['departamento']
        telefono=request.form['telefono']
        ciudad=request.form['ciudad']
        colegio=request.form['colegio']
        alumnos=request.form['alumnos']
        id=request.form['id']
        if institucion=='' or representante=='' or email==''or departamento==''or telefono==''or ciudad=='' or alumnos=='' :
            flash('Todos los datos son OBLIGATORIOS...')
        else:
            #actualizando los datos
            User.query.filter_by(id=id).update(dict(institucion=institucion))
            User.query.filter_by(id=id).update(dict(representante=representante))
            User.query.filter_by(id=id).update(dict(email=email))
            User.query.filter_by(id=id).update(dict(departamento=departamento))
            User.query.filter_by(id=id).update(dict(telefono=telefono))
            User.query.filter_by(id=id).update(dict(ciudad=ciudad))
            User.query.filter_by(id=id).update(dict(colegio=colegio))
            User.query.filter_by(id=id).update(dict(alumnos=alumnos))
            flash('Los datos Fueron ACTUALIZADOS con exito !')
            db.session.commit()
    count = File.get_by_count(dataUser.id)
    count_delete = File.get_by_count_delete(dataUser.id)
    return render_template('/edit-register.html',dataUser = dataUser, count=count, count_delete=count_delete, tgg = totalGeneralGenero(dataUser.id),
        tge = totalGeneralEstudiantes(dataUser.id))
    #return render_template('/edit-register.html',dataUser = dataUser )


@app.route("/delete-file",methods=['GET', 'POST'])
def delete_file():
    #validando que el usuario tenga una sesión abierta
    dataUser = User.get_by_email(session['email'])
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        id_file=request.form['id_file']
        File.query.filter_by(id=id_file).update(dict(state="0"))
        db.session.commit()
        flash('El Archivo fue eliminado con exito !')
    return redirect('files')



@app.route("/chage-password",methods=['GET', 'POST'])
def chage_password():
    dataUser = User.get_by_email(session['email'])
    currentPassword=request.form['currentPassword']
    newPassword=request.form['newPassword']
    confirmNewPassword=request.form['confirmNewPassword']
    print(f"contraseña ingresada >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<: {currentPassword}")
    if request.method == 'POST' and request.form['updateRegister'] == "updatePass":
        #organizando terminos para generación de contraseña encryptada
        currentPassword = "".join([(str(ord(x)-96) if x.isalpha() else x) for x in list(currentPassword)])
        currentPassword = int(currentPassword)

        encrypNewPass = "".join([(str(ord(x)-96) if x.isalpha() else x) for x in list(newPassword)])
        encrypNewPass = int(newPassword)
        #encryptando contraseña ingresada por uausuario
        encrypPass = User._encryptSuperHard(Alpha.alpha().lower(),currentPassword)
        encrypNewPass = User._encryptSuperHard(Alpha.alpha().lower(),encrypNewPass)
        #encryptando contraseña ingresada con la contraseña de la base de datos
        if dataUser.password == encrypPass :
            if confirmNewPassword == newPassword:
                User.query.filter_by(id=dataUser.id).update(dict(password=encrypNewPass))
                db.session.commit()
                print(f"acepta confirmación de contraseñas iguales : {dataUser.id}")
            else:
                flash('La nueva contraseña  y confirmar contraseña no son iguales, intentelo de nuevo !')
        else:
            flash('Los contraseña actual ingresada no es correcta !')

    count = File.get_by_count(dataUser.id)
    count_delete = File.get_by_count_delete(dataUser.id)
    return redirect('/edit-register')
    # return render_template('/edit-register.html',dataUser = dataUser, count=count, count_delete=count_delete)

   # return render_template('/edit-register.html',dataUser = dataUser)


#acceso a folder
@app.route('/upload/<newFile>')
def upload(newFile):
   return send_from_directory(app.config['FOLDER'],newFile)

@app.route("/files",methods=['GET', 'POST'])
def files():
    #validando que el usuario tenga una sesión abierta
    if 'email' not in session:
        return redirect(url_for('login'))
    dataUser = User.get_by_email(session['email'])
    if request.method == 'POST':

        file=request.files['file']
        comentario=request.form['comentario']
        grupo=request.form['grupo']

        if grupo=='' or file=='' :
            flash('El archivo de EXCEL es Obligatorio...')
            return redirect(url_for('files'))

        #formato de hora para imagenes
        now=datetime.now()
        time=now.strftime("%Y%H%M%S")
        #guardando imagen

        if file.filename!='':
            newFile=time+'-{}_'.format(dataUser.id)+secure_filename(file.filename)
            #newFile=time+file.filename
            file.save("upload/"+newFile)
            _upload  =  File(
            archivo =  newFile,
            comentario = comentario,
            grupo  = grupo,
            state  = "1",
            user_id  = int(dataUser.id),

            )
            db.session.add(_upload)
            db.session.commit()
            flash('El archivo a sido subido correctamente...')

    files_all = File.get_by_all_files(dataUser.id)
    count = File.get_by_count(dataUser.id)
    count_delete = File.get_by_count_delete(dataUser.id)
    if count<1  :
        count = 0
        count_delete = 0
    return render_template('/files.html',dataUser = dataUser, files=files_all, count=count, count_delete=count_delete,  tgg = totalGeneralGenero(dataUser.id),
        tge = totalGeneralEstudiantes(dataUser.id))

@app.route("/register",methods=['GET', 'POST'])
def register():
    #ojo :: https://j2logo.com/tutorial-flask-leccion-5-base-de-datos-con-flask-sqlalchemy/
    login_register = forms.FormRegister(request.form)
    if request.method == 'POST' and login_register.validate():
        email = login_register.email.data
        user = User.get_by_email(email)
        if user is not None:
            error_message= 'El email {} ya está siendo utilizado por otro usuario'.format(email)
            flash(error_message)
        else:
            user  =  User(
            login_register.password.data,
            login_register.email.data,
            login_register.institucion.data,
            login_register.representante.data,
            login_register.departamento.data,
            login_register.telefono.data,
            login_register.ciudad.data,
            login_register.direccion.data,
            login_register.colegio.data,
            login_register.alumnos.data
            )
            db.session.add(user)
            db.session.commit()
            print("logra validación guarda en db users")
            success_message= 'Por favor inicie sesión con los datos ingresados...'
            flash(success_message)
            return redirect('/')

    if request.method == 'POST' and request.form.get("password", False) != request.form.get("confirmPassword", False):
        success_message= 'Confirmación de contraseña invalida !'
        flash(success_message)

    return render_template(
        'register.html', form = login_register,
         institucion=request.form.get("institucion", False),
         representante=request.form.get("representante", False),
         email=request.form.get("email", False),
         departamento=request.form.get("departamento", False),
         telefono=request.form.get("telefono", False),
         ciudad=request.form.get("ciudad", False),
         direccion=request.form.get("direccion", False),
         colegio=request.form.get("colegio", False),
         alumnos=request.form.get("alumnos", False),


         )

    #ajax route
@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    print (request.form)
    username =  request.form['email']
    response= {'status':200, 'username':username, 'id':1}
    return json.dumps(response)



if __name__ == '__main__':

    csrf.init_app(app)
    db.init_app(app)
    #contexto
    with app.app_context():
        db.create_all()
    app.run( port=5000)
