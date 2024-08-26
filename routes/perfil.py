<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect,url_for, flash
import json
from firebaseAuth import  atualiza_perfilfb
=======
from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb
import json



>>>>>>> e5b00452ef9a9d24f1acb157770fb59547bfa1c3
perfil_routes = Blueprint('perfil', __name__)

""" Rotas de perfil
    - /perfil - Get - Retorna a página de perfil
    - /perfil/editar - PUT - Retorna a página de edição de perfil
    - /perfil/editar - POST - Edita o perfil do usuário
    - /perfil/excluir - DELETE - Exclui o perfil do usuário
"""

@perfil_routes.route('/', methods=['GET','DELETE','POST'])
def pagina_perfil():
<<<<<<< HEAD
    """ Retorna a página de perfil """
    
    def inputs_perfil():
        imputs = [
            {'id': 'nome', 'type': 'text', 'placeholder': 'Nome', 'name': 'nome'},
            {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
            {'id': 'senha', 'type': 'senha', 'placeholder': 'Senha', 'name': 'senha'}
        ]
        if request.method == 'POST':
            data = request.form
        try:
            atualiza_perfilfb(data['nome'], data['email'], data['senha'])  # tem que fazer essa função
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('perfil.perfil'))
        except Exception as e:
            error_message = json.loads(e.args[1])['error']['message']
            flash(error_message, 'danger')
            return render_template('perfil.html', inputs=inputs_perfil())

    return render_template('perfil.html', inputs=inputs_perfil())
    
=======
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
                # recoverPassword(user['email'])
                flash('Email de recuperação de senha enviado!', 'success')
            except Exception as e:
                print(e)
                # Captura a exceção e imprime a mensagem de erro
                # error_message = json.loads(e.args[1])['error']['message']
                # flash(error_message, 'danger')
                # return render_template('perfil.html', inputs=inputs)
        
        else:
            try:
                db.child("usuarios").child(user_email).remove()  # Exclui o perfil do usuário
                flash('Perfil excluído com sucesso!', 'success')
                return redirect(url_for('login.pagina_login'))  # Redireciona para a página de login
            except Exception as e:
                error_message = json.loads(e.args[1])['error']['message']
                flash(error_message, 'danger')
                return redirect(url_for('perfil.pagina_perfil'))
            
    return render_template('perfil.html', inputs=inputs, text=text)

>>>>>>> e5b00452ef9a9d24f1acb157770fb59547bfa1c3
