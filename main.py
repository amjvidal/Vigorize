from flask import Flask, render_template
from routes.login import login_routes
from routes.recuperar import recuperar_routes
from routes.cadastro import cadastro_routes

app = Flask(__name__)

app.register_blueprint(login_routes)
app.register_blueprint(recuperar_routes)
app.register_blueprint(cadastro_routes)

app.run(debug=True)
