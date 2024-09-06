from flask import Flask, request
app = Flask(__name__)
app.secret_key = 'vigorizee'

from routes.home import home_routes
from routes.login import login_routes
from routes.recuperar import recuperar_routes
from routes.cadastro import cadastro_routes
from routes.perfil import perfil_routes
from routes.primeiroAcesso import primeiroAcesso_routes

app.register_blueprint(home_routes)
app.register_blueprint(login_routes, url_prefix='/login')
app.register_blueprint(recuperar_routes, url_prefix='/recuperar')
app.register_blueprint(cadastro_routes, url_prefix='/cadastro')
app.register_blueprint(perfil_routes, url_prefix='/perfil')
app.register_blueprint(primeiroAcesso_routes, url_prefix='/primeiroAcesso')


app.run(debug=True)
