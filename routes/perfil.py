from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from firebaseAuth import recoverPassword, db, auth, emailDb
import json
from calculadora import calculaTMB, calculaPercentGorduraMASC, calculaPercentGorduraFem, calculaIMC
from datetime import datetime

def calcular_idade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    data_atual = datetime.now()
    idade = data_atual.year - data_nascimento.year
    if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade

perfil_routes = Blueprint('perfil', __name__)

@perfil_routes.route('/', methods=['GET', 'POST'])
def pagina_perfil():
    user = auth.current_user

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
        data_nas_user = db.child("usuarios").child(user_email).child("data").get().val()
        fisicos = ["Sedentário", "Atividade Ligeira", "Atividade Moderada", "Atividade Intensa", "Atividade Muito Intensa"]
        atividade_user = db.child("usuarios").child(user_email).child("fisico").get().val()

        inputs = [
            {'id': 'altura', 'type': 'number', 'value': altura_user, 'name': 'altura', 'label': 'Altura(cm)', 'max': '250', 'min': '100'},
            {'id': 'peso', 'type': 'number', 'value': peso_user, 'name': 'peso', 'label': 'Peso(kg)', 'max': '500', 'min': '30'},
            {'id': 'cintura', 'type': 'number', 'value': cintura_user, 'name': 'cintura', 'label': 'Cintura(cm)', 'max': '180', 'min': '30'},
            {'id': 'pescoco', 'type': 'number', 'value': pescoco_user, 'name': 'pescoco', 'label': 'Pescoço(cm)', 'max': '60', 'min': '20'}
        ]

        if sexo_user == 'Feminino':
            quadril_user = db.child("usuarios").child(user_email).child("quadril").get().val()
            inputs.append({'id': 'quadril', 'type': 'number', 'value': quadril_user, 'name': 'quadril', 'label': 'Quadril(cm)', 'max': '180', 'min': '30'})

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
                         'pescoco': data['pescoco'],
                         'fisico': data['fisico']})
                    flash('Perfil atualizado com sucesso!', 'success')

                    return redirect(url_for('perfil.pagina_perfil'))
                except Exception as e:
                    error_message = json.loads(e.args[1])['error']['message']
                    flash(error_message, 'danger')
                    return redirect(url_for('perfil.pagina_perfil'))
            elif action == 'recover_password':
                try:
                    recoverPassword(user['email'])
                    flash('Email de recuperação de senha enviado!', 'success')
                except Exception as e:
                    print(e)

            elif action == 'delete_account':
                try:
                    auth.delete_user_account(user['idToken'])
                    db.child("usuarios").child(user_email).remove()
                    flash('Perfil excluído com sucesso!', 'success')
                    return redirect(url_for('login.pagina_login'))
                except Exception as e:
                    error_message = str(e)
                    flash(error_message, 'danger')
                    return redirect(url_for('perfil.pagina_perfil'))

    except Exception as e:
        flash('Erro ao acessar o perfil.', 'danger')
        return redirect(url_for('login.pagina_login'))

    idade = calcular_idade(data_nas_user)

    Caloria = round(calculaTMB(int(peso_user), int(altura_user), int(idade), sexo_user, atividade_user), 4)
    max_Caloria = 10000
    CaloriaMedia = (Caloria / max_Caloria) * 100
    if sexo_user == 'Masculino':
        percent_gordura = calculaPercentGorduraMASC(int(altura_user), int(cintura_user), int(pescoco_user))
    else:
        percent_gordura = calculaPercentGorduraFem(int(altura_user), int(cintura_user), int(pescoco_user), int(quadril_user))

    imc = calculaIMC(int(peso_user), int(altura_user))

    # Salvar os dados calculados no Firebase
    db.child("usuarios").child(user_email).update(
        {
            'imc': imc,
            'percent_gordura': percent_gordura,
            'Caloria': Caloria
        }
    )

    return render_template('perfil.html', inputs=inputs, percent_gordura=percent_gordura, imc=imc, fisicos=fisicos, CaloriaMedia=CaloriaMedia, idade=idade, Caloria=Caloria, atividade_user=atividade_user)
