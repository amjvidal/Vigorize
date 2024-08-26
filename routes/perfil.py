from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb
import json



perfil_routes = Blueprint('perfil', __name__)

""" Rotas de perfil
    - /perfil - Get - Retorna a página de perfil
    - /perfil/editar - PUT - Retorna a página de edição de perfil
    - /perfil/editar - POST - Edita o perfil do usuário
    - /perfil/excluir - DELETE - Exclui o perfil do usuário
"""

@perfil_routes.route('/', methods=['GET','POST'])
def pagina_perfil():
    user=auth.current_user
    user_email = emailDb(user['email'])
    name_user = db.child("usuarios").child(user_email).child("nome").get().val()
    text = [
        {'id': user['email']}
    ]
    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': name_user,'name': 'nome'},
    ]

    if request.method == 'POST':
        user=auth.current_user
        user_email = emailDb(user['email'])
        name_user = db.child("usuarios").child(user_email).child("nome").get().val()
        action = request.form.get('action')
        data = request.form
        if action == 'update_name':
            try:
                db.child("usuarios").child(user_email).update({'nome': data['nome']})
                print("Nome atualizado com sucesso!")
                flash('Nome de perfil atualizado com sucesso!', 'success')
                return redirect(url_for('perfil.pagina_perfil'))
            except Exception as e:
                # Captura a exceção e imprime a mensagem de erro
                error_message = json.loads(e.args[1])['error']['message']
                flash(error_message, 'danger')
                return redirect(url_for('perfil.pagina_perfil'))
        elif action == 'recover_password':
            try:
                recoverPassword(user['email'])
                flash('Email de recuperação de senha enviado!', 'success')
            except Exception as e:
                print(e)
                # Captura a exceção e imprime a mensagem de erro
                # error_message = json.loads(e.args[1])['error']['message']
                # flash(error_message, 'danger')
                # return render_template('perfil.html', inputs=inputs)
        
        elif action == 'delete_account':
            try:
                auth.delete_user_account(user['idToken'])  # Exclui o usuário da autenticação
                db.child("usuarios").child(user_email).remove()  # Exclui o perfil do usuário
                flash('Perfil excluído com sucesso!', 'success')
                return redirect(url_for('login.pagina_login'))  # Redireciona para a página de login
            except Exception as e:
                error_message = str(e)
                flash(error_message, 'danger')
                return redirect(url_for('perfil.pagina_perfil'))
            
    return render_template('perfil.html', inputs=inputs, text=text)