import json
from flask import Blueprint, render_template, request, redirect,url_for, flash
from firebaseAuth import loginfb, auth, db, emailDb, firstLogin


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
                    flash('Email não verificado, foi enviado um email de verificação para o seu e-mail !', 'danger')
                    return redirect(url_for('login.pagina_login'))
                
                is_admin = db.child("usuarios").child(emailDb(data['email'])).get().val().get('is_admin', False)
                if is_admin:
                    return redirect(url_for('admin.admin_dashboard'))
                

                if firstLogin(data['email']):
                    flash('Primeiro acesso, por favor complete seu cadastro!', 'success')
                    return redirect(url_for('primeiroAcesso.primeiroAcesso'))
                return redirect(url_for('perfil.pagina_perfil'))
            
            except Exception as e:
                error_message = str(e)
                print(error_message)
                if "INVALID_LOGIN_CREDENTIALS" in error_message:
                    error_message = "Email ou senha inválidos !"
                flash(error_message, 'danger')
                return redirect(url_for('login.pagina_login'))
        
        else:
            auth.current_user = None
            flash('Logout realizado com sucesso!', 'success')
            return redirect(url_for('login.pagina_login'))
        
    if user:
        flash('Você já está logado!', 'info')
    
        is_admin = db.child("usuarios").child(emailDb(user['email'])).get().val().get('is_admin', False)
        if is_admin:
            return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('perfil.pagina_perfil'))
    
    return render_template('login.html', inputs=inputs)

