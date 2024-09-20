from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth2, emailDb, storage, img_url_firebase, armazenar_dados_mensais
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for
from calculadora import  calculaIMC

imc_routes = Blueprint('imc', __name__)

@imc_routes.route('/', methods=['GET', 'POST'])
def pagina_calculadora_imc():
    imc_result = None
    user = auth2.current_user

    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    user_id = emailDb(user['email'])
    user_data = db.child("usuarios").child(user_id).get().val()
    profile_picture_url = user_data.get('profilePicture', None)

    
    if request.method == 'POST':
        data = request.form
        action = data.get('action')

        try:
            if action == 'calcular_imc':
                altura = float(request.form.get('altura')) / 100  # Converte para metros
                peso = float(request.form.get('peso'))
                imc_result = (calculaIMC(peso, altura))/10000
                
                # flash(f'Seu IMC é: {imc_result:.2f}', 'success')

            elif action == 'recover_password':
                try:
                    recoverPassword(user['email'])
                    flash('Email de recuperação de senha enviado!', 'success')
                except Exception as e:
                    error_message = str(e)
                    flash(error_message, 'danger')
                    return redirect(url_for('imc.pagina_calculadora_imc'))

            elif action == 'delete_account':
                try:
                    auth2.delete_user_account(user['idToken'])  # Exclui o usuário da autenticação
                    db.child("usuarios").child(user_id).remove()  # Exclui o perfil do usuário
                    auth2.current_user = None
                    flash('Perfil excluído com sucesso!', 'success')
                    return redirect(url_for('login.pagina_login'))
                except Exception as e:
                    error_message = str(e)
                    flash(error_message, 'danger')
                    return redirect(url_for('imc.pagina_calculadora_imc'))
            
            elif action == 'save_profile':

                from firebaseAuth import profilePics_folder

                if not os.path.exists(profilePics_folder):
                    os.makedirs(profilePics_folder)  

                if 'file' not in request.files:
                    flash('Nenhum arquivo selecionado.')
                    return redirect(url_for('imc.pagina_calculadora_imc'))
                
                file = request.files['file']

                if file.filename == '':
                    flash('Nenhum arquivo selecionado.')
                    return redirect(url_for('imc.pagina_calculadora_imc'))
                
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
                        return redirect(url_for('imc.pagina_calculadora_imc'))
                    except Exception as e:
                        error_message = str(e)
                        print(error_message)
                        flash("Erro ao salvar a imagem", 'danger')
                        return redirect(url_for('imc.pagina_calculadora_imc'))
                    
        except ValueError:
            flash('Por favor, insira valores válidos para altura e peso.', 'danger')

    return render_template('calculadora_imc.html', imc_result=imc_result, profile_picture_url=profile_picture_url)
