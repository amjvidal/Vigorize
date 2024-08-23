from flask import Blueprint, render_template

cadastro_routes = Blueprint('cadastro', __name__)

""" Rotas de cadastro
    - /cadastro - Get - Retorna a página de cadastro
    - /cadastro - Post - Realiza o cadastro do usuário e evnia um email de confirmação
    - /cadastro/<id_usuario>/autentificação - Get - Vai para a página de autentificação
    - /cadastro/<id_usuario>/autentificação/<id_usuario> - Post - Realiza a autentificação do usuário
    - / - Get - Retorna a página de login
    - /recuperar - Get - Retorna a página de recuperação de senha
"""

@cadastro_routes.route('/cadastro')
def cadastro():
    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': 'Digite seu nome'},
        {'id': 'email', 'type': 'email', 'placeholder': 'Email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha'},
        {'id': 'confirmaSenha', 'type': 'password', 'placeholder': 'Confirme sua senha'}
    ]
    return render_template('cadastro.html', inputs=inputs)
