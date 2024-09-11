from flask import Flask
# from flask_cors import CORS
from firebaseAuth import profilePics_folder
app = Flask(__name__)
# CORS(app)
app.secret_key = 'vigorizee'

from routes.home import home_routes
from routes.login import login_routes
from routes.recuperar import recuperar_routes
from routes.cadastro import cadastro_routes
from routes.perfil import perfil_routes
from routes.primeiroAcesso import primeiroAcesso_routes
from routes.perGordura import perGordura_routes
from routes.imc import imc_routes
from routes.tabelaNutricional import tabelaNutricao
from routes.admin import admin_routes
from routes.cadastroadmin import cadastroadmin_routes
from routes.loginadmin import loginadmin_routes

app.config['UPLOAD_FOLDER'] = profilePics_folder

app.register_blueprint(home_routes)
app.register_blueprint(login_routes, url_prefix='/login')
app.register_blueprint(tabelaNutricao, url_prefix='/tabelaNutricional')
app.register_blueprint(recuperar_routes, url_prefix='/recuperar')
app.register_blueprint(cadastro_routes, url_prefix='/cadastro')
app.register_blueprint(perfil_routes, url_prefix='/perfil')
app.register_blueprint(primeiroAcesso_routes, url_prefix='/primeiro-acesso')
app.register_blueprint(perGordura_routes, url_prefix='/percentual-gordura')
app.register_blueprint(imc_routes, url_prefix='/imc')
app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(cadastroadmin_routes, url_prefix='/cadastroadmin')
app.register_blueprint(loginadmin_routes, url_prefix='/loginadmin')


app.run(debug=True)
