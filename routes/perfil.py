from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb
import json
from calculadora import calculaTMB, calculaPercentGorduraMASC, calculaPercentGorduraFem
from datetime import datetime




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

    altura_user = db.child("usuarios").child(user_email).child("altura").get().val()
    peso_user = db.child("usuarios").child(user_email).child("peso").get().val()
    cintura_user = db.child("usuarios").child(user_email).child("cintura").get().val()
    pescoco_user = db.child("usuarios").child(user_email).child("pescoco").get().val()
    sexo_user = db.child("usuarios").child(user_email).child("sexo").get().val()
    idade_user = db.child("usuarios").child(user_email).child("dataNas").get().val()
    atividade_user = db.child("usuarios").child(user_email).child("fisico").get().val()
    
    
    # def calcular_idade(idade_user):
 
    #     try:
    #         # Converter a data de nascimento para um objeto datetime
    #         data_nascimento = datetime.strptime(idade_user, '%Y-%m-%d')
    #     except ValueError:
    #         raise ValueError("A data de nascimento deve estar no formato 'YYYY-MM-DD'")
        
    #     # Obter a data atual
    #     hoje = datetime.today()

    #     # Calcular a diferença de anos
    #     idade = hoje.year - data_nascimento.year

    #     # Ajustar se a data de nascimento ainda não ocorreu neste ano
    #     if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
    #         idade -= 1

    #     return idade
    
    # idade = calcular_idade(idade_user)

    inputs = [
        {'id': 'altura', 'type': 'number', 'value': altura_user,'name': 'altura', 'label': 'Altura(cm)','max': '250','min': '100'},
        {'id': 'peso', 'type': 'number', 'value': peso_user,'name': 'peso', 'label': 'Peso(kg)','max': '500','min': '30'},
        {'id': 'cintura', 'type': 'number', 'value': cintura_user,'name': 'cintura', 'label': 'Cintura(cm)','max': '180','min': '30'},
        {'id': 'pescoco', 'type': 'number', 'value': pescoco_user,'name': 'pescoco', 'label': 'Pescoço(cm)','max': '60','min': '20'},
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
    gor_value = calculaPercentGorduraMASC(int(altura_user), int(cintura_user), int(pescoco_user))
    cal_value = calculaTMB(int(peso_user), int(altura_user),  idade, sexo_user, atividade_user)
    cal_valuefm = calculaPercentGorduraFem(int(altura_user), int(cintura_user), int(pescoco_user), int(quadril_user))
    

    #     elif action == 'recover_password':
    #         try:
    #             recoverPassword(user['email'])
    #             flash('Email de recuperação de senha enviado!', 'success')
    #         except Exception as e:
    #             print(e)
    #             # Captura a exceção e imprime a mensagem de erro
    #             # error_message = json.loads(e.args[1])['error']['message']
    #             # flash(error_message, 'danger')
    #             # return render_template('perfil.html', inputs=inputs)
        
    #     elif action == 'delete_account':
    #         try:
    #             auth.delete_user_account(user['idToken'])  # Exclui o usuário da autenticação
    #             db.child("usuarios").child(user_email).remove()  # Exclui o perfil do usuário
    #             flash('Perfil excluído com sucesso!', 'success')
    #             return redirect(url_for('login.pagina_login'))  # Redireciona para a página de login
    #         except Exception as e:
    #             error_message = str(e)
    #             flash(error_message, 'danger')
    #             return redirect(url_for('perfil.pagina_perfil'))
    
    
            
    return render_template('perfil.html', inputs=inputs, gor_value=gor_value)

