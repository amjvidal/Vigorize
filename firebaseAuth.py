import pyrebase
from flask import flash

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

def cadastrofb(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
    except:
        #Deve aparecer uma popup aqui na pagina dizendo que o email ja existe
        # Tentei aqui mas n ta funcionando @everyone alguem arruma
        # isso aqui n funciona:
        flash("Você já está cadastrado, por favor faça o login")
        
def loginfb(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
    except:
        # PopUp dnv dizendo que o usuario não esta cadastrado (tratar dps com if pra ver se é a senha q ta errada)
        # isso aqui n funciona:
        flash('Usuario ja cadastrado')