from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
from firebaseAuth import cadastrofb

cadastro_routes = Blueprint('cadastro', __name__)

""" Rotas de cadastro
    - /cadastro - Get - Retorna a página de cadastro
    - /cadastro - Post - Realiza o cadastro do usuário e evnia um email de confirmação
    - /cadastro/<id_usuario>/autentificação - Get - Vai para a página de autentificação
    - /cadastro/<id_usuario>/autentificação - Post - Realiza a autentificação do usuário
"""

@cadastro_routes.route('/', methods=['GET', 'POST'])
def cadastro():
    """ Retorna a página de cadastro """
    # Define os inputs da página de cadastro
    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': 'Digite seu nome', 'name': 'nome'},
        {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha'},
        {'id': 'confirmaSenha', 'type': 'password', 'placeholder': 'Confirme sua senha', 'name': 'confirmaSenha'}
    ]

    if request.method == 'POST':
        data = request.form
        
        if data['senha'] != data['confirmaSenha']:
            flash('senhas não coencidem', 'danger')
            return render_template('cadastro.html', inputs=inputs)
        try:
            cadastrofb(data['nome'],data['email'], data['senha'])
            flash('Foi enviado um email de verificação para: '+data['email']+' !', 'success')
            return redirect(url_for('login.pagina_login'))
        except Exception as e:
            # Captura a exceção e imprime a mensagem de erro
            error_message = json.loads(e.args[1])['error']['message']
            flash(error_message, 'danger')
            return render_template('cadastro.html', inputs=inputs) 

    return render_template('cadastro.html', inputs=inputs)