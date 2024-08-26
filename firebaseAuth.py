import pyrebase
from flask import flash
import requests

config = {
    'apiKey': "AIzaSyD4JXX-udSB_3dQrzfmqS5Bop0VEdiThUo",
    'authDomain': "vigorize-3d6cf.firebaseapp.com",
    'databaseURL': "https://vigorize-3d6cf-default-rtdb.firebaseio.com/",
    'projectId': "vigorize-3d6cf",
    'storageBucket': "vigorize-3d6cf.appspot.com",
    'messagingSenderId': "385997478942",
    'appId': "1:385997478942:web:dc73f225e95938034fe20f",
    'measurementId': "G-N2ETEHJM8N"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

def cadastrofb(nome, email, password):
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])
        data={'nome':nome,
              'email':email}
        db.child('usuarios').child(remove_pontos(email)).set(data)
        
def loginfb(email, password):
        user = auth.sign_in_with_email_and_password(email, password)
        user_info = auth.get_account_info(user['idToken'])

        # Verifica se o e-mail está verificado
        email_verified = user_info['users'][0]['emailVerified']
        if email_verified == False:
            auth.current_user = None
            return email_verified
        
def recoverPassword(email):
    auth.send_password_reset_email(email)

def remove_pontos(texto):
    return texto.replace(".", "@")

