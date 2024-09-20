import pyrebase 
import firebase_admin
from firebase_admin import credentials, auth
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


try:
    cred = credentials.Certificate("vigorize-3d6cf-firebase-adminsdk-ixlbs-e3264553cc.json")
    firebase_admin.initialize_app(cred)
except:
    pass

profilePics_folder = 'profile_pics'
firebase = pyrebase.initialize_app(config)
auth2 = firebase.auth()
storage = firebase.storage()
db = firebase.database()

def cadastrofb(nome, email, password, dataNas):
    # Criar usuário no Firebase Auth
    user = auth2.create_user_with_email_and_password(email, password)
    
    # Enviar email de verificação
    auth2.send_email_verification(user['idToken'])
    localId = user['localId']
    
    # Definir os dados do usuário, incluindo is_admin como False
    data = {
        'localId': localId,
        'nome': nome,
        'email': email,
        'data': dataNas,
        'firstTime': True,
        'is_admin': False  # Usuários não são administradores por padrão
    }
    
    # Salvar os dados do usuário no Firebase Realtime Database
    db.child('usuarios').child(remove_pontos(email)).set(data)


def loginfb(email, password):
        user = auth2.sign_in_with_email_and_password(email, password)
        user_info = auth2.get_account_info(user['idToken'])
        # Verifica se o e-mail está verificado
        email_verified = user_info['users'][0]['emailVerified']
        if email_verified == False:
            auth2.send_email_verification(user['idToken'])
            auth2.current_user = None
            return email_verified
        
def enviarDadosDb(user_email, altura, peso, sexo, fisico):
    data = {
        'altura': altura,
        'peso': peso,
        'sexo': sexo,
        'fisico': fisico,
        'firstTime': False}
    return db.child("usuarios").child(user_email).update(data)
        
def recoverPassword(email):
    auth2.send_password_reset_email(email)

def remove_pontos(texto):
    return texto.replace(".", "@")

def emailDb(email):
    return remove_pontos(email).lower()

def firstLogin(email):
    user_email = emailDb(email)
    firstLogin = db.child("usuarios").child(user_email).child("firstTime").get().val()
    return firstLogin

def set_persistence_local(): #pessitencia de login
    auth2.set_persistence(firebase.auth.Auth.Persistence.LOCAL)
    
    
def armazenar_dados_mensais(user_email, mes, ano, calorias, imc, percent_gordura):
    data = {
        'calorias': calorias,
        'imc': imc,
        'percent_gordura': percent_gordura
    }
    db.child("usuarios").child(user_email).child("dados_mensais").child(f"{ano}-{mes}").set(data)

def img_url_firebase(url):
    for i in range((len(url)-1), 0, -1):
        # Retirar até o %
        if url[i] == '%':
            url = url[:i]
            break
    # Acessar o link
    response = requests.get(url)
    token = response.json()['downloadTokens']
    url = url + "?alt=media&token=" + token
    return url

