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

    user = auth.current_user

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
                is_admin = db.child("usuarios").child(emailDb(data['email'])).get().val().get('is_admin', False)
                if email_verified == False:
                    flash('Email não verificado, por favor verifique seu email!', 'danger')
                    return redirect(url_for('login.pagina_login'))
                
                if is_admin:
                    return redirect(url_for('admin.admin_dashboard'))
                

                if firstLogin(data['email']):
                    return redirect(url_for('primeiroAcesso.primeiroAcesso'))
                
                
                return redirect(url_for('perfil.pagina_perfil'))
            except Exception as e:
                error_message = json.loads(e.args[1])['error']['message']
                flash(error_message, 'danger')
                return redirect(url_for('login.pagina_login'))
        
        else:
            auth.current_user = None
            flash('Logout realizado com sucesso!', 'success')
            return redirect(url_for('login.pagina_login'))
        
    if user:
        is_admin = db.child("usuarios").child(emailDb(user['email'])).get().val().get('is_admin', False)
        if is_admin:
            return redirect(url_for('admin.admin_dashboard'))
        print("não admin")
        return redirect(url_for('perfil.pagina_perfil'))
    
    return render_template('login.html', inputs=inputs)

