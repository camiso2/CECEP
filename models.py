from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from config import Alpha
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy import desc

from sqlalchemy import ForeignKey



db = SQLAlchemy()

class File(db.Model):
    __tablename__='files'
    id=db.Column(db.Integer, primary_key=True)
    archivo = db.Column(db.String(255))
    comentario = db.Column(db.String(255), nullable=True)
    grupo = db.Column(db.String(50))
    state = db.Column(db.String(10))
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self,archivo,comentario,grupo,state,user_id):
        self.archivo = archivo
        self.comentario = comentario
        self.grupo = grupo
        self.state = state
        self.user_id = user_id

    @staticmethod
    def get_by_all_files(dataUser):
        return File.query.filter_by(user_id=dataUser).order_by(File.id.desc()).all()

    @staticmethod
    def get_by_all_files_state(dataUser):
        return File.query.filter_by(user_id=dataUser, state="1").all()
    
    @staticmethod
    def get_by_file(file):
        return File.query.filter_by(id=file).first()

    @staticmethod
    def get_by_count(dataUser):
        return File.query.filter_by(user_id=dataUser, state="1").count()
        
    @staticmethod
    def get_by_count_delete(dataUser):
        return File.query.filter_by(user_id=dataUser, state="0").count()
       


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    institucion = db.Column(db.String(50))
    representante = db.Column(db.String(50))
    departamento = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    ciudad = db.Column(db.String(50))
    direccion = db.Column(db.String(80))
    colegio = db.Column(db.String(80))
    alumnos = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    
    def __init__(self,password,email,institucion,representante,departamento,telefono,ciudad,direccion,colegio,alumnos):
        #self.password = self.__create_password(password)
        password = "".join([(str(ord(x)-96) if x.isalpha() else x) for x in list(password)])
        password = int(password)
        self.password = User._encryptSuperHard(Alpha.alpha().lower(),password)
        self.email = email
        self.institucion = institucion
        self.representante = representante
        self.departamento = departamento
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion
        self.colegio = colegio
        self.alumnos = alumnos

    
    def _encryptSuperHard(cleartext, password):
        cyphertext = ""
        for char in cleartext:
            if char in Alpha.alpha():
                newpos = (Alpha.alpha().find(char) + password) % 26
                cyphertext += Alpha.alpha()[newpos]
            else:
                cyphertext += char

        return cyphertext

    def decryptSuperHard(cleartext,password):
        cyphertext = ""
        
        for char in cleartext:
            if char in Alpha.alpha():
                newpos = (Alpha.alpha().find(char) - password) % 26
                cyphertext += Alpha.alpha()[newpos]
            else:
                cyphertext += char

        return cyphertext

        
    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
        #return  true / false

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_password(password):
        return User.query.filter_by(password=password).first()
    
   