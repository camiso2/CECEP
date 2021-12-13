import os

alpha = 'qwertyuioplkjhgfdsazxcvbnm/*-+$%&/()=?¿Ç'

class Config(object):
    SECRET_KEY=alpha

class DevelopentConfig(Config):
    DEBUG= True
    SQLALCHEMY_DATABASE_URI='mysql://root:@localhost/cecep'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class Alpha():
    def alpha():
        return alpha