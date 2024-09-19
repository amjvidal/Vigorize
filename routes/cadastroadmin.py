from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import auth, db, emailDb
import json

cadastroadmin_routes = Blueprint('cadastroadmin', __name__)

@cadastroadmin_routes.route('/', methods=['GET', 'POST'])
def register_admin():
    user = auth.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    is_admin = db.child("usuarios").child(emailDb(user['email'])).get().val().get('is_admin', False)
    if not is_admin:
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('perfil.pagina_perfil'))
    
    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': 'Digite o nome do administrador', 'name': 'nome', 'block': 'block'},
        {'id': 'email', 'type': 'email', 'placeholder': 'Email do administrador', 'name': 'email', 'block': 'block'},
        {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha', 'block': 'block'},
        {'id': 'confirmaSenha', 'type': 'password', 'placeholder': 'Confirme a senha', 'name': 'confirmaSenha', 'block': 'block'},
    ]

    if request.method == 'POST':
        data = request.form

        if len(data['senha']) < 6 or len(data['senha']) > 15:
            flash('A senha deve ter entre 6 e 15 caracteres', 'danger')
            return render_template('register_admin.html', inputs=inputs)
        
        if data['senha'] != data['confirmaSenha']:
            flash('As senhas não coincidem', 'danger')
            return render_template('register_admin.html', inputs=inputs)

        try:
            # Registrar o administrador
            new_admin = auth.create_user_with_email_and_password(data['email'], data['senha'])
            
            # Enviar e-mail de verificação
            auth.send_email_verification(new_admin['idToken'])
            
            user_id = emailDb(data['email'])
            
            # Atualizar a informação de administrador no banco de dados
            db.child("usuarios").child(user_id).set({
                'nome': data['nome'],
                'email': data['email'],
                'is_admin': True
            })
            
            flash('Administrador cadastrado com sucesso! Verifique seu e-mail para confirmar a conta.', 'success')
            return redirect(url_for('cadastroadmin.admin_dashboard'))  
        except Exception as e:
            # Verifique o tipo de e.args[1]
            error_message = e.args[1] if isinstance(e.args[1], str) else e.args[1].get('error', {}).get('message', 'Erro desconhecido')
            flash(f'Erro: {error_message}', 'danger')

    return render_template('register_admin.html', inputs=inputs)
