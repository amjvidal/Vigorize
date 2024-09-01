from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb
import json

perGordura_routes = Blueprint('perGordura', __name__)

""" Rotas de perGordura
    - /perGordura - Get - Retorna a página de perGordura
    - /perGordura/editar - POST - Edita o perGordura do usuário
"""
@perGordura_routes.route('/', methods=['GET','POST'])
def pagina_perGordura():
    user=auth.current_user
    user_email = emailDb(user['email'])
    user_sexo = db.child("usuarios").child(user_email).child("sexo").get().val()

    inputs = [
        {'id': 'cintura', 'type': 'number', 'placeholder': "Cintura(cm)",'name': 'cintura', 'label': 'Cintura(cm)','max': '180','min': '30'},
        {'id': 'pescoco', 'type': 'number', 'placeholder': "Pescoço(cm)",'name': 'pescoco', 'label': 'Pescoço(cm)','max': '500','min': '30'},
    ]
    if user_sexo == 'Feminino':
        inputs.append({'id': 'quadril', 'type': 'number', 'placeholder': "Quadril(cm)",'name': 'quadril', 'label': 'Quadril(cm)', 'max': '180','min': '30'})

    if request.method == 'POST':
        data = request.form
        action = data.get('action')

        if action == 'enviar_dados':
            try:
                if data['cintura'] == '':
                    data['cintura'] = None
                if data['pescoco'] == '':
                    data['pescoco'] = None
                if user_sexo == 'Feminino':
                    if data['quadril'] == '':
                        data['quadril'] = None
                    db.child("usuarios").child(user_email).update(
                        {'cintura': data['cintura'],
                         'pescoco': data['pescoco'],
                         'quadril': data['quadril']
                        })
                else:
                    db.child("usuarios").child(user_email).update(
                        {'cintura': data['cintura'],
                        'pescoco': data['pescoco'],
                        'quadril': None
                        })
                flash('Dados enviados com sucesso!', 'success')
                return redirect(url_for('perfil.pagina_perfil'))
            except Exception as e:
                flash('Erro ao atualizar gordura!', 'danger')
                return redirect(url_for('perGordura.perGordura'))
        
        if action == "pular":
            try:
                db.child("usuarios").child(user_email).update(
                    {'cintura': None,
                    'pescoco': None,
                    'quadril': None
                    })
                
                flash('Dados não enviados!', 'success')
                return redirect(url_for('perfil.pagina_perfil'))
            except Exception as e:
                flash('Erro ao atualizar gordura!', 'danger')
                return redirect(url_for('perGordura.perGordura'))

    return render_template('perGordura.html', inputs = inputs)