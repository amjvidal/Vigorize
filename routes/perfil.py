from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb, storage, img_url_firebase, armazenar_dados_mensais
import os, json
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for
from calculadora import calculaTMB, calculaPercentGorduraMASC, calculaPercentGorduraFem, calculaIMC, calcular_idade

perfil_routes = Blueprint('perfil', __name__)

@perfil_routes.route('/', methods=['GET', 'POST'])
def pagina_perfil():
    user = auth.current_user

    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))

    try:
        user_id = emailDb(user['email'])
        user_data = db.child("usuarios").child(user_id).get().val()
        profile_picture_url = user_data.get('profilePicture', None)
        altura_user = db.child("usuarios").child(user_id).child("altura").get().val()
        peso_user = db.child("usuarios").child(user_id).child("peso").get().val()
        cintura_user = db.child("usuarios").child(user_id).child("cintura").get().val()
        pescoco_user = db.child("usuarios").child(user_id).child("pescoco").get().val()
        sexo_user = db.child("usuarios").child(user_id).child("sexo").get().val()
        atividade_user = db.child("usuarios").child(user_id).child("fisico").get().val()
        data_nas_user = db.child("usuarios").child(user_id).child("data").get().val()
        fisicos = ["Sedentário", "Atividade Ligeira", "Atividade Moderada", "Atividade Intensa", "Atividade Muito Intensa"]

        inputs = [
            {'id': 'altura', 'type': 'number', 'value': altura_user, 'name': 'altura', 'label': 'Altura(cm)', 'max': '250', 'min': '100'},
            {'id': 'peso', 'type': 'number', 'value': peso_user, 'name': 'peso', 'label': 'Peso(kg)', 'max': '500', 'min': '30'},
            {'id': 'cintura', 'type': 'number', 'value': cintura_user, 'name': 'cintura', 'label': 'Cintura(cm)', 'max': '180', 'min': '30'},
            {'id': 'pescoco', 'type': 'number', 'value': pescoco_user, 'name': 'pescoco', 'label': 'Pescoço(cm)', 'max': '60', 'min': '20'}
        ]

        if sexo_user == 'Feminino':
            quadril_user = db.child("usuarios").child(user_id).child("quadril").get().val()
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
                    
                    db.child("usuarios").child(user_id).update(
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
                    # Captura a exceção e imprime a mensagem de erro
                    # error_message = json.loads(e.args[1])['error']['message']
                    # flash(error_message, 'danger')
                    # return render_template('perfil.html', inputs=inputs, fisicos=fisicos)
            elif action == 'delete_account':
                try:
                    auth.delete_user_account(user['idToken'])  # Exclui o usuário da autenticação
                    db.child("usuarios").child(user_id).remove()  # Exclui o perfil do usuário
                    flash('Perfil excluído com sucesso!', 'success')
                    return redirect(url_for('login.pagina_login'))
                except Exception as e:
                    error_message = str(e)
                    flash(error_message, 'danger')
                    return redirect(url_for('perfil.pagina_perfil'))
            
            elif action == 'save_profile':

                from firebaseAuth import profilePics_folder

                if not os.path.exists(profilePics_folder):
                    os.makedirs(profilePics_folder)  

                if 'file' not in request.files:
                    flash('Nenhum arquivo selecionado.')
                    return redirect(url_for('perfil.pagina_perfil'))
                
                file = request.files['file']

                if file.filename == '':
                    flash('Nenhum arquivo selecionado.')
                    return redirect(url_for('perfil.pagina_perfil'))
                
                if file:
                    try:

                        # Salva a imagem no diretório local
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(profilePics_folder, filename)
                        file.save(file_path)

                        # Salva a imagem no storage do Firebase
                        storage.child(f"profile_pics/{user_id}").put(file_path)

                        # URL da imagem
                        blob = storage.child(f"profile_pics/{user_id}/{filename}")
                        url = blob.get_url(None)
                        download_url = img_url_firebase(url)

                        # Salvar a URL no Firebase Realtime Database
                        db.child("usuarios").child(user_id).update({
                            'profilePicture': download_url
                        })
                        
                        os.remove(file_path)

                        flash('Foto de perfil atualizada com sucesso!', 'success')
                        return redirect(url_for('perfil.pagina_perfil'))
                    except Exception as e:
                        error_message = str(e)
                        print(error_message)
                        flash("Erro ao salvar a imagem", 'danger')
                        return redirect(url_for('perfil.pagina_perfil'))
    


    except Exception as e:
        error_message = str(e)
        print(error_message)
        flash('Erro ao acessar o perfil.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    #cal_tmb = calculaTMB(int(peso_user),int(altura_user) ,int(idade_user), sexo_user, atividade_user)

    idade = calcular_idade(data_nas_user)
    Caloria = round(calculaTMB(int(peso_user), int(altura_user), int(idade), sexo_user, atividade_user), 4)
    max_Caloria = 10000
    CaloriaMedia = (Caloria / max_Caloria) * 100

    if sexo_user == 'Masculino':
        percent_gordura = calculaPercentGorduraMASC(int(altura_user), int(cintura_user), int(pescoco_user))
    else:
        percent_gordura = calculaPercentGorduraFem(int(altura_user), int(cintura_user), int(pescoco_user), int(quadril_user))

    imc = calculaIMC(int(peso_user), int(altura_user))
            


    # Armazenar os dados mensais
    hoje = datetime.now()
    mes_atual = hoje.strftime("%m")
    ano_atual = hoje.strftime("%Y")
    armazenar_dados_mensais(user_id, mes_atual, ano_atual, Caloria, imc, percent_gordura)

    # Buscar os dados mensais para o gráfico
    dados_mensais = db.child("usuarios").child(user_id).child("dados_mensais").get().val()
    labels = []
    calorias_data = []
    imc_data = []
    percent_gordura_data = []

    if dados_mensais:
        for mes, dados in dados_mensais.items():
            labels.append(mes)
            calorias_data.append(dados['calorias'])
            imc_data.append(dados['imc'])
            percent_gordura_data.append(dados['percent_gordura'])

    return render_template('perfil.html', 
                           inputs=inputs, 
                           percent_gordura=percent_gordura, 
                           imc=imc, fisicos=fisicos, 
                           atividade_user=atividade_user, 
                           profile_picture_url=profile_picture_url)
    