from flask import Flask, request
from firebaseAuth import profilePics_folder
app = Flask(__name__)
app.secret_key = 'vigorizee'


from routes.login import login_routes
from routes.recuperar import recuperar_routes
from routes.cadastro import cadastro_routes
from routes.perfil import perfil_routes
from routes.primeiroAcesso import primeiroAcesso_routes
from routes.perGordura import perGordura_routes
from routes.imc import imc_routes


app.config['UPLOAD_FOLDER'] = profilePics_folder

app.register_blueprint(login_routes)
app.register_blueprint(recuperar_routes, url_prefix='/recuperar')
app.register_blueprint(cadastro_routes, url_prefix='/cadastro')
app.register_blueprint(perfil_routes, url_prefix='/perfil')
app.register_blueprint(primeiroAcesso_routes, url_prefix='/primeiro-acesso')
app.register_blueprint(perGordura_routes, url_prefix='/perGordura')
app.register_blueprint(imc_routes, url_prefix='/imc')


app.run(debug=True)
