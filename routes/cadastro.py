from flask import Blueprint, render_template, request
from database.usuarios import USUARIOS
from firebaseAuth import cadastrofb

cadastro_routes = Blueprint('cadastro', __name__)

""" Rotas de cadastro
    - /cadastro - Get - Retorna a página de cadastro
    - /cadastro - Post - Realiza o cadastro do usuário e evnia um email de confirmação
    - /cadastro/<id_usuario>/autentificação - Get - Vai para a página de autentificação
    - /cadastro/<id_usuario>/autentificação - Post - Realiza a autentificação do usuário
"""

@cadastro_routes.route('/')
def pagina_cadastro():
    """ Retorna a página de cadastro """
    # Define os inputs da página de cadastro
    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': 'Digite seu nome', 'name': 'nome'},
        {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha'},
        {'id': 'confirmaSenha', 'type': 'password', 'placeholder': 'Confirme sua senha', 'name': 'confirmaSenha'}
    ]
    return render_template('cadastro.html', inputs=inputs)

@cadastro_routes.route('/', methods=['POST'])
def cadastra():
    """ Realiza o cadastro do usuário e envia um email de confirmação """
    data = request.json

    if data['senha'] != data['confirmaSenha']:
        return {'message': 'As senhas não conferem!'}, 400
    
    novo_usuario = {
        'id': len(USUARIOS) + 1,
        'nome': data['nome'],
        'email': data['email'],
        'senha': data['senha']
    }
    cadastrofb(data['email'], data['senha'])

    # implementar o fire base AQUI !!!!!


    return {'message': 'Usuário cadastrado com sucesso!'}, 201

@cadastro_routes.route('/<int:id_usuario>/autentificacao')
def pagina_autentificacao(id_usuario):
    """ Vai para a página de autentificação """
    return render_template('form_autentificacao.html')

@cadastro_routes.route('/<int:id_usuario>/autentificacao', methods=['POST'])
def autentifica(id_usuario):
    """ Realiza a autentificação do usuário """
    pass