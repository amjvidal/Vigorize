from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
from firebaseAuth import cadastrofb, set_persistence_local


cadastro_routes = Blueprint('cadastro', __name__)

""" Rotas de cadastro
    - /cadastro - Get - Retorna a página de cadastro
    - /cadastro - Post - Realiza o cadastro do usuário e evnia um email de confirmação
    - /cadastro/<id_usuario>/autentificação - Get - Vai para a página de autentificação
    - /cadastro/<id_usuario>/autentificação - Post - Realiza a autentificação do usuário
"""

@cadastro_routes.route('/', methods=['GET', 'POST'])
def cadastro():
    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': 'Digite seu nome', 'name': 'nome', 'block': 'block'},
        {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email', 'block': 'block'},
        {'id': 'dataNas', 'type': 'date', 'placeholder': 'dd.mm.yyyy', 'name': 'dataNas', 'max': '2015-12-31', 'min': '1924-01-01', 'block': 'block'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha', 'block': 'block'},
        {'id': 'confirmaSenha', 'type': 'password', 'placeholder': 'Confirme sua senha', 'name': 'confirmaSenha', 'block': 'block'},
        {'id': 'termo', 'type': 'checkbox', 'name': 'termo', 'value': 'aceito', 'block': 'inline'},
    ]
    
    if request.method == 'POST':
        data = request.form
        if data['senha'] != data['confirmaSenha']:
            flash('Senhas não coencidem !', 'danger')
            return render_template('cadastro.html', inputs=inputs)
        try:
            cadastrofb(data['nome'], data['email'], data['senha'], data['dataNas'])
            flash('Foi enviado um email de verificação para: ' + data['email'] + ' !', 'success')
            return redirect(url_for('login.pagina_login'))
        except Exception as e:
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
               error_message= 'Email já cadastrado !'
            if "WEAK_PASSWORD" in error_message:
               error_message= 'Senha precisa ter no mínimo 6 caracteres !'
            if "TOO_MANY_ATTEMPTS" in error_message:
               error_message= 'Muitas tentativas, tente mais tarde !'
            
            flash(error_message, 'danger')
            return render_template('cadastro.html', inputs=inputs)
        
    return render_template('cadastro.html', inputs=inputs)