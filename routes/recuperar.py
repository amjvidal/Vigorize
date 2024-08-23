from flask import Blueprint, render_template

recuperar_routes = Blueprint('recuperar', __name__)

""" Rotas de recuperação de senha
    - /recuperar - Get - Retorna a página de recuperação de senha
    - /recuperar - Post - Envia um email de recuperação de senha
    - /recuperar/<id_usuario>/trocarSenha - Get - Retorna a página de troca de senha
    - /recuperar/<id_usuario>/trocarSenha - Post - Troca a senha do usuário
"""

@recuperar_routes.route('/')
def pagina_recuperar():
    """ Retorna a página de recuperação de senha """
    # Define os inputs da página de recuperação de senha
    inputs = [
        {'id': 'nome', 'type': 'email', 'placeholder': 'Digite seu email'}
    ]
    return render_template('recuperar.html', inputs=inputs)

@recuperar_routes.route('/', methods=['POST'])
def recupera():
    """ Envia um email de recuperação de senha """
    pass

@recuperar_routes.route('/<int:id_usuario>/trocarSenha')
def pagina_trocarSenha(id_usuario):
    """ Vai para a página de trocar senha """
    return render_template('form_trocaSenha.html')

@recuperar_routes.route('/<int:id_usuario>/trocarSenha', methods=['PUT'])
def trocaSenha(id_usuario):
    """ Troca a senha do usuário """
    pass