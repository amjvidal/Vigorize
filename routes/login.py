from flask import Blueprint, render_template

login_routes = Blueprint('login', __name__)

""" Rotas de login
    - / - Get - Retorna a página de login
    - / - Post - Realiza o login do usuário
    - /recuperar - Get - Retorna a página de recuperação de senha
    - /cadastro - Get - Retorna a página de cadastro
"""

@login_routes.route('/')
def index():
    inputs = [
        {'id': 'email', 'type': 'email', 'placeholder': 'Email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha'}
    ]
    return render_template('index.html', inputs=inputs)