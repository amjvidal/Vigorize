from flask import Flask, request
app = Flask(__name__)
app.secret_key = 'vigorizee'

from routes.login import login_routes
from routes.recuperar import recuperar_routes
from routes.cadastro import cadastro_routes
from routes.perfil import perfil_routes

app.register_blueprint(login_routes)
app.register_blueprint(recuperar_routes, url_prefix='/recuperar')
app.register_blueprint(cadastro_routes, url_prefix='/cadastro')
app.register_blueprint(perfil_routes, url_prefix='/perfil')


app.run(debug=True)
