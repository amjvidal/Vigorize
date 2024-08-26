from flask import Blueprint, render_template, request, redirect,url_for
from firebaseAuth import loginfb

login_routes = Blueprint('login', __name__)

""" Rotas de login
    - / - Get - Retorna a página de login
    - / - Post - Verifica o login do usuário
    - /home - Get - Retorna a página home
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
    try:
        loginfb(data['email'], data['senha'])
    except:
        return {'message': 'Falha no login!'}, 400

    return redirect(url_for('perfil.pagina_perfil'), code=200)