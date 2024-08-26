from flask import Blueprint, render_template, request, redirect,url_for, flash
import json
from firebaseAuth import loginfb

login_routes = Blueprint('login', __name__)

""" Rotas de login
    - / - Get - Retorna a página de login
    - / - Post - Verifica o login do usuário
    - /home - Get - Retorna a página home
"""

@login_routes.route('/', methods=['GET','POST'])
def pagina_login():
    """ Retorna a página de login """
    # Define os inputs da página de login
    inputs = [
        {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha'}
    ]
    if request.method == 'POST':
        data = request.form
        try:
            loginfb(data['email'], data['senha'])
            flash('Usuário logado com sucesso!', 'success')
            return redirect(url_for('perfil.pagina_perfil'))
        except Exception as e:
            # Captura a exceção e imprime a mensagem de erro
            error_message = json.loads(e.args[1])['error']['message']
            flash(error_message, 'danger')
            return render_template('index.html', inputs=inputs)
        
    return render_template('index.html', inputs=inputs)