from flask import Flask, render_template
from routes.login import login
from routes.cadastro import cadastro
from routes.recuperar import recuperar
app = Flask(__name__)

@app.route('/')
def index():
    inputs = [
        {'id': 'email', 'type': 'email', 'placeholder': 'Digite seu email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Digite sua senha'}
    ]
    return render_template('index.html', inputs=inputs)

@app.route("/recuperar")
def recuperar():
    return render_template('recuperar.html')

@app.route('/cadastro')
def cadastro():
    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': 'Digite seu nome'},
        {'id': 'email', 'type': 'email', 'placeholder': 'Digite seu email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Digite sua senha'},
        {'id': 'confirmaSenha', 'type': 'password', 'placeholder': 'Confirme sua senha'}
    ]
    return render_template('cadastro.html', inputs=inputs)

app.run(debug=True)
