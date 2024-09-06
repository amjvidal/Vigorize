import json
from flask import Blueprint, render_template, request, redirect,url_for, flash
from firebaseAuth import loginfb, auth, db, emailDb, firstLogin, set_persistence_local


login_routes = Blueprint('login', __name__)

""" Rotas de login
    - / - Get - Retorna a página de login
    - / - Post - Verifica o login do usuário
    - /home - Get - Retorna a página home
"""

@login_routes.route('/', methods=['GET', 'POST'])
def pagina_login():
    inputs = [
        {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha'}
    ]
    if request.method == 'POST':
        action = request.form.get('action')
        data = request.form
        if action == 'login':
            try:
                email_verified = loginfb(data['email'], data['senha'])
                if email_verified == False:
                    flash('Email não verificado, por favor verifique seu email!', 'danger')
                    return render_template('index.html', inputs=inputs)

                if firstLogin(data['email']):
                    return redirect(url_for('primeiroAcesso.primeiroAcesso'))
                
                return redirect(url_for('perfil.pagina_perfil'))
            except Exception as e:
                error_message = json.loads(e.args[1])['error']['message']
                flash(error_message, 'danger')
                return render_template('index.html', inputs=inputs)
        else:
            auth.current_user = None
            flash('Logout realizado com sucesso!', 'success')
            return render_template('index.html', inputs=inputs)
    
    if auth.current_user:
        return redirect(url_for('perfil.pagina_perfil'))
    
    return render_template('index.html', inputs=inputs)