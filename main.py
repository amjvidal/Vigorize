from flask import Flask
from routes.login import login_routes
from routes.recuperar import recuperar_routes
from routes.cadastro import cadastro_routes
app = Flask(__name__)
app.secret_key = 'vigorizee'

app.register_blueprint(login_routes)
app.register_blueprint(recuperar_routes, url_prefix='/recuperar')
app.register_blueprint(cadastro_routes, url_prefix='/cadastro')
app.register_blueprint(perfil_routes, url_prefix='/perfil')

app.run(debug=True)
