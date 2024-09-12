from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb, storage, img_url_firebase, armazenar_dados_mensais
import os, json
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for
import datetime
admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/', methods=['GET'])
def admin_dashboard():
    user = auth.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))

    # Verificar se o usuário é administrador
    user_id = emailDb(user['email'])
    user_data = db.child("usuarios").child(user_id).get().val()

    if not user_data.get('is_admin', False):
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('perfil.pagina_perfil'))

    # Buscar todos os usuários cadastrados
    all_users = db.child("usuarios").get().val()
    print(user)
    return render_template('admin_dashboard.html', users=all_users)

@admin_routes.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user_data = db.child("usuarios").child(user_id).get().val()

    if request.method == 'POST':
        data = request.form
        try:
            db.child("usuarios").child(user_id).update({
                'altura': data['altura'],
                'peso': data['peso'],
                'cintura': data['cintura'],
                'fisico': data['fisico'],
                
                
            })
            flash('Dados atualizados com sucesso!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')

    return render_template('edit_user.html', user=user_data, user_id=user_id)

@admin_routes.route('/admin/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        user_data = db.child("usuarios").child(user_id).get().val()
        
        auth.delete_user_account(user_data['idToken'])
        db.child("usuarios").child(user_id).remove()
        flash('Usuário excluído com sucesso!', 'success')
    except Exception as e:
        error_message = str(e)
        flash(error_message, 'danger')

    return redirect(url_for('admin.admin_dashboard'))

@admin_routes.route('/admin/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    user_data = db.child("usuarios").child(user_id).get().val()
    if user_data is None:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('user_details.html', user=user_data, user_id=user_id)
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
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Nenhuma imagem selecionada.', 'danger')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('Nenhuma imagem selecionada.', 'danger')
            return redirect(request.url)

        if file:
            try:
                # Salva a imagem no diretório local
                filename = secure_filename(file.filename)
                file_path = os.path.join('static/uploads/', filename)
                file.save(file_path)

                # Salva a imagem no storage do Firebase
                storage.child(f"profile_pics/{user_id}/{filename}").put(file_path)

                # Obtém a URL da imagem
                blob = storage.child(f"profile_pics/{user_id}/{filename}")
                url = blob.get_url(None)

                # Atualiza a URL no Firebase Realtime Database
                db.child("usuarios").child(user_id).update({
                    'profile_image': url
                })

                # Remove o arquivo local
                os.remove(file_path)

                flash('Imagem de perfil atualizada com sucesso!', 'success')
                return redirect(url_for('admin.user_details', user_id=user_id))
            except Exception as e:
                error_message = str(e)
                print(error_message)
                flash("Erro ao salvar a imagem", 'danger')
                return redirect(url_for('admin.user_details', user_id=user_id))

    return render_template('upload_image.html', user_id=user_id)

@admin_routes.route('/admin/toggle_user/<user_id>', methods=['POST'])
def toggle_user(user_id):
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
        auth.current_user = None
        flash('Você saiu com sucesso.', 'success')
    except Exception as e:
        flash(f'Ocorreu um erro ao sair: {str(e)}', 'danger')
    return redirect(url_for('login.pagina_login'))