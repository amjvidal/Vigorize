from flask import Blueprint, render_template, request, flash, redirect, url_for, session
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

    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    try:
        user_email = emailDb(user['email'])
        altura_user = db.child("usuarios").child(user_email).child("altura").get().val()
        peso_user = db.child("usuarios").child(user_email).child("peso").get().val()
        cintura_user = db.child("usuarios").child(user_email).child("cintura").get().val()
        pescoco_user = db.child("usuarios").child(user_email).child("pescoco").get().val()
        sexo_user = db.child("usuarios").child(user_email).child("sexo").get().val()
        atividade_user = db.child("usuarios").child(user_email).child("fisico").get().val()
        fisicos = ["Sedentário", "Atividade Ligeira", "Atividade Moderada", "Atividade Intensa", "Atividade Muito Intensa"]

        inputs = [
            {'id': 'altura', 'type': 'number', 'value': altura_user, 'name': 'altura', 'label': 'Altura(cm)', 'max': '250', 'min': '100'},
            {'id': 'peso', 'type': 'number', 'value': peso_user, 'name': 'peso', 'label': 'Peso(kg)', 'max': '500', 'min': '30'},
            {'id': 'cintura', 'type': 'number', 'value': cintura_user, 'name': 'cintura', 'label': 'Cintura(cm)', 'max': '180', 'min': '30'},
<<<<<<< HEAD
            {'id': 'pescoco', 'type': 'number', 'value': pescoco_user, 'name': 'pescoco', 'label': 'Pescoço(cm)', 'max': '60', 'min': '20'}
=======
            {'id': 'pescoco', 'type': 'number', 'value': pescoco_user, 'name': 'pescoco', 'label': 'Pescoço(cm)', 'max': '60', 'min': '20'},
            {'id': 'sexo', 'type': 'text', 'value': sexo_user, 'name': 'sexo', 'label': 'Sexo', 'disabled': 'true'},
            {'id': 'fisico', 'type': 'text', 'value': atividade_user, 'name': 'fisico', 'label': 'Atividade Física', 'disabled': 'true'},
            {'id': 'idade', 'type': 'number', 'value': idade_user, 'name': 'idade', 'label': 'Idade', 'max': '120', 'min':15}
            
>>>>>>> parent of dbc6221 (Atualizar campo "idade" para "dataNas" na página de perfil)
            
        ]
        if sexo_user == 'Feminino':
            quadril_user = db.child("usuarios").child(user_email).child("quadril").get().val()
            inputs.append({'id': 'cintura', 'type': 'number', 'value': quadril_user,'name': 'cintura', 'label': 'Quadril(cm)', 'max': '180','min': '30'})

        if request.method == 'POST':
            action = request.form.get('action')
            data = request.form

            if action == 'update_profile':
                try:
                    if data['altura'] == '':
                        data['altura'] = altura_user
                    if data['peso'] == '':
                        data['peso'] = peso_user
                    if data['cintura'] == '':
                        data['cintura'] = cintura_user
                    if data['pescoco'] == '':
                        data['pescoco'] = pescoco_user
                    if sexo_user == 'Feminino':
                        if data['quadril'] == '':
                            data['quadril'] = quadril_user
                    
                    db.child("usuarios").child(user_email).update(
                        {'altura': data['altura'],
                        'peso': data['peso'],
                        'cintura': data['cintura'],
                        'pescoco': data['pescoco']})
                    flash('Perfil atualizado com sucesso!', 'success')

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
                    # return render_template('perfil.html', inputs=inputs, fisicos=fisicos)
            
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
                
    except Exception as e:
        flash('Erro ao acessar o perfil.', 'danger')
        return redirect(url_for('login.pagina_login'))
            
    return render_template('perfil.html', inputs=inputs, fisicos=fisicos)