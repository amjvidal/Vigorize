from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth2, emailDb, storage, img_url_firebase, armazenar_dados_mensais
import os, json
from firebase_admin import auth
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for
import datetime
admin_routes = Blueprint('admin', __name__)
import requests

@admin_routes.route('/', methods=['GET'])
def admin_dashboard():
    user = auth2.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))

    # Verificar se o usuário é administrador
    user_id = emailDb(user['email'])
    user_data = db.child("usuarios").child(user_id).get().val()

    if not user_data.get('is_admin', False):
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))

    
    all_users = db.child("usuarios").get().val()
    users_not_admin = {}
    for user_id, user_data in all_users.items():
        if not user_data.get('is_admin', False):
            user_data['id'] = user_id
            users_not_admin[user_id] = user_data
        
    return render_template('admin_dashboard.html', users=users_not_admin)

@admin_routes.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = auth2.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    

    user_data = db.child("usuarios").child(user_id).get().val()
    altura_user = db.child("usuarios").child(user_id).child("altura").get().val()
    peso_user = db.child("usuarios").child(user_id).child("peso").get().val()
    cintura_user = db.child("usuarios").child(user_id).child("cintura").get().val()
    pescoco_user = db.child("usuarios").child(user_id).child("pescoco").get().val()
    sexo_user = db.child("usuarios").child(user_id).child("sexo").get().val()
    fisicos = ["Sedentário", "Ligeira", "Moderada", "Intensa", "Muito Intensa"]

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
        data = request.form
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
            if sexo_user == 'Feminino':
                db.child("usuarios").child(user_id).update({'quadril': data['quadril']})
            flash('Perfil atualizado com sucesso!', 'success')

        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')

        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit_user.html', user=user_data, user_id=user_id, inputs=inputs, fisicos=fisicos)

@admin_routes.route('/admin/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = auth2.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    try:
        localId = db.child("usuarios").child(user_id).child("localId").get().val()
        auth.delete_user(localId)
        db.child("usuarios").child(user_id).remove()

        flash('Usuário excluído com sucesso!', 'success')
        
    except Exception as e:
        error_message = str(e)
        print(error_message)
        flash(error_message, 'danger')

    return redirect(url_for('admin.admin_dashboard'))

@admin_routes.route('/admin/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    user_data = db.child("usuarios").child(user_id).get().val()
    email_user = db.child("usuarios").child(user_id).child("email").get().val()
    nome_user = db.child("usuarios").child(user_id).child("nome").get().val()
    altura_user = db.child("usuarios").child(user_id).child("altura").get().val()
    peso_user = db.child("usuarios").child(user_id).child("peso").get().val()
    cintura_user = db.child("usuarios").child(user_id).child("cintura").get().val()
    pescoco_user = db.child("usuarios").child(user_id).child("pescoco").get().val()
    sexo_user = db.child("usuarios").child(user_id).child("sexo").get().val()
    fisico_user = db.child("usuarios").child(user_id).child("fisico").get().val()
        
    fisicos = ["Sedentário", "Ligeira", "Moderada", "Intensa", "Muito Intensa"]

    datas = [
            {'id': 'email', 'value': email_user, 'label': 'E-mail'},
            {'id': 'nome', 'value': nome_user, 'label': 'Nome'},
            {'id': 'altura', 'type': 'number', 'value': altura_user, 'name': 'altura', 'label': 'Altura(cm)', 'max': '250', 'min': '100'},
            {'id': 'peso', 'type': 'number', 'value': peso_user, 'name': 'peso', 'label': 'Peso(kg)', 'max': '500', 'min': '30'},
            {'id': 'cintura', 'type': 'number', 'value': cintura_user, 'name': 'cintura', 'label': 'Cintura(cm)', 'max': '180', 'min': '30'},
            {'id': 'pescoco', 'type': 'number', 'value': pescoco_user, 'name': 'pescoco', 'label': 'Pescoço(cm)', 'max': '60', 'min': '20'},
            {'id': 'fisico', 'type': 'select', 'value': fisico_user, 'name': 'fisico', 'label': 'Nível de atividade física',},
            {'id': 'sexo', 'value': sexo_user, 'label': 'Sexo'} 
            ]

    if sexo_user == 'Feminino':
        quadril_user = db.child("usuarios").child(user_id).child("quadril").get().val()
        datas.append({'id': 'quadril', 'type': 'number', 'value': quadril_user, 'name': 'quadril', 'label': 'Quadril(cm)', 'max': '180', 'min': '30'})

    if user_data is None:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('user_details.html', user=user_data, user_id=user_id, datas=datas, fisicos=fisicos)
def get_current_date_path():
    now = datetime.now()
    year_month = now.strftime('%Y-%m')
    return year_month

def get_user_data(user_id):
    # Ajuste o caminho para a pasta onde os dados estão armazenados
    user_ref = db.reference(f'usuarios/{user_id}/dados_mensais/year_month')
    user_data = user_ref.get()
    return user_data


@admin_routes.route('/admin/upload_image/<user_id>', methods=['GET', 'POST'])
def upload_image(user_id):
    user = auth2.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))

    profile_picture_url = db.child("usuarios").child(user_id).get().val().get('profilePicture', None)

    if request.method == 'POST':
        action = request.form.get('action')

        from firebaseAuth import profilePics_folder

        if action == 'upload_image':

            if not os.path.exists(profilePics_folder):
                os.makedirs(profilePics_folder)

            if 'file' not in request.files:
                flash('Nenhum arquivo selecionado.')
                return redirect(url_for('admin.upload_image', user_id=user_id))
            
            file = request.files['file']

            if file.filename == '':
                flash('Nenhum arquivo selecionado.')
                return redirect(url_for('admin.upload_image', user_id=user_id))
            
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
                    return redirect(url_for('admin.upload_image', user_id=user_id))
                
                except Exception as e:
                    error_message = str(e)
                    print(error_message)
                    flash("Erro ao salvar a imagem", 'danger')
                    return redirect(url_for('admin.upload_image', user_id=user_id))
                
        elif action == 'delete_image':
            try:
                # Referência ao caminho da foto de perfil no Firebase
                user_ref = db.child("usuarios").child(user_id).get()
                profile_pic_url = user_ref.val().get('profilePicture', None)

                if profile_pic_url and "profile_pics" in profile_pic_url:
                    # Extrair o URL do arquivo
                    file_url = profile_pic_url.split('?')[0] 
                    print(f"URL do arquivo extraído: {file_url}")

                    # Construir o URL para deletar o arquivo
                    file_path = file_url.replace('https://firebasestorage.googleapis.com/v0/b/', '')
                    api_url = f"https://firebasestorage.googleapis.com/v0/b/{file_path}?alt=media"
                    print(f"URL da API para deletar: {api_url}")

                    # Fazer a requisição DELETE
                    response = requests.delete(api_url)
                    if response.status_code == 204:
                        print("Imagem removida do Firebase Storage")

                        # Remove a URL da foto de perfil do Firebase Realtime Database
                        db.child("usuarios").child(user_id).update({
                            'profilePicture': None
                        })
                        flash('Foto de perfil removida com sucesso!', 'success')
                    else:
                        print(f"Erro ao remover a imagem: {response.status_code} - {response.text}")
                        flash('Erro ao remover a foto de perfil.', 'danger')
                else:
                    flash('Nenhuma foto de perfil encontrada para remover.', 'warning')

            except Exception as e:
                error_message = str(e)
                print(f"Erro ao remover a imagem: {error_message}")
                flash('Erro ao remover a foto de perfil.', 'danger')

        
    return render_template('upload_image.html', user_id=user_id, profile_picture_url=profile_picture_url)

@admin_routes.route('/admin/toggle_user/<user_id>', methods=['POST'])
def toggle_user(user_id):
    user = auth2.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    user_data = db.child("usuarios").child(user_id).get().val()
    if user_data is None:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    is_blocked = user_data.get('is_blocked', False)
    db.child("usuarios").child(user_id).update({'is_blocked': not is_blocked})

    status = 'bloqueado' if not is_blocked else 'desbloqueado'
    flash(f'Usuário {status} com sucesso!', 'success')
    return redirect(url_for('admin.user_details', user_id=user_id))

@admin_routes.route('/admin/reset_password/<user_id>', methods=['POST'])
def reset_password(user_id):
    user = auth2.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    try:
        user_data = db.child("usuarios").child(user_id).get().val()
        if user_data is None:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('admin.admin_dashboard'))
        
        user_email = user_data['email']
        recoverPassword(user_email)
        
        flash('Instruções para redefinir a senha foram enviadas ao e-mail do usuário.', 'success')
    except Exception as e:
        flash(f'Ocorreu um erro: {str(e)}', 'danger')

    return redirect(url_for('admin.user_details', user_id=user_id))

@admin_routes.route('/logout', methods=['POST'])
def logout():
    try:
        # Limpar a sessão do usuário
        auth2.current_user = None
        flash('Você saiu com sucesso.', 'success')
    except Exception as e:
        flash(f'Ocorreu um erro ao sair: {str(e)}', 'danger')
    return redirect(url_for('login.pagina_login'))