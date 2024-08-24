from flask import Blueprint, render_template, request
from firebaseAuth import loginfb

login_routes = Blueprint('login', __name__)

""" Rotas de login
    - / - Get - Retorna a página de login
    - / - Post - Realiza o login do usuário
    - /recuperar - Get - Retorna a página de recuperação de senha
    - /cadastro - Get - Retorna a página de cadastro
"""

@login_routes.route('/')
def pagina_login():
    """ Retorna a página de login """
    # Define os inputs da página de login
    inputs = [
        {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha'}
    ]
    return render_template('index.html', inputs=inputs)

@login_routes.route('/', methods=['POST'])
def loga():
    """ Realiza o login do usuário """
    data = request.json
    
    loginfb(data['email'], data['senha'])
    return render_template('cadastro.html')