from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb
import json

perfil_routes = Blueprint('perfil', __name__)

@perfil_routes.route('/', methods=['GET', 'POST', 'DELETE'])
def pagina_perfil():
    user = auth.current_user
    if not user:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))

    user_email = emailDb(user['email'])
    name_user = db.child("usuarios").child(user_email).child("nome").get().val()

    text = [{'id': user['email']}]
    inputs = [{'id': 'nome', 'type': 'text', 'placeholder': name_user, 'name': 'nome'}]

    if request.method == 'POST':
        action = request.form.get('action')
        data = request.form
        if action == 'update_name':
            try:
                db.child("usuarios").child(user_email).update({'nome': data['nome']})
                flash('Nome de perfil atualizado com sucesso!', 'success')
                return redirect(url_for('perfil.pagina_perfil'))
            except Exception as e:
                error_message = str(e)
                flash(error_message, 'danger')
                return redirect(url_for('perfil.pagina_perfil'))
        elif action == 'recover_password':
            try:
                recoverPassword(user['email'])
                flash('Email de recuperação de senha enviado!', 'success')
            except Exception as e:
                error_message = str(e)
                flash(error_message, 'danger')
        
    elif request.method == 'DELETE':
        try:
            db.child("usuarios").child(user_email).remove()  # Exclui o perfil do usuário
            auth.delete_user(user['uid'])  # Exclui o usuário da autenticação
            flash('Perfil excluído com sucesso!', 'success')
            return redirect(url_for('login.pagina_login'))  # Redireciona para a página de login
        except Exception as e:
            error_message = str(e)
            flash(error_message, 'danger')
            return redirect(url_for('perfil.pagina_perfil'))
            
    return render_template('perfil.html', inputs=inputs, text=text)
