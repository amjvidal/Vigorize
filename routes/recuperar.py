from flask import Blueprint, render_template

recuperar_routes = Blueprint('recuperar', __name__)

""" Rotas de recuperação de senha
    - /recuperar - Get - Retorna a página de recuperação de senha
    - /recuperar - Post - Envia um email de recuperação de senha
    - /recuperar/<id_usuario>/trocarSenha - Get - Retorna a página de troca de senha
    - /recuperar/<id_usuario>/trocarSenha - Post - Troca a senha do usuário
    - / - Get - Retorna a página de login
    - /cadastro - Get - Retorna a página de cadastro
"""

@recuperar_routes.route('/recuperar')
def recuperar():
    inputs = [
        {'id': 'nome', 'type': 'email', 'placeholder': 'Digite seu email'}
    ]
    return render_template('recuperar.html', inputs=inputs)  