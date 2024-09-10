from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import recoverPassword, db, auth, emailDb, storage, img_url_firebase, armazenar_dados_mensais
import os, json
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests

admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/', methods=['GET'])
def admin_dashboard():
    user = auth.current_user
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))

    # Verificar se o usuário é administrador (deve ser configurado na criação do usuário)
    user_id = emailDb(user['email'])
    user_data = db.child("usuarios").child(user_id).get().val()

    if not user_data.get('is_admin', False):
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('perfil.pagina_perfil'))

    # Buscar todos os usuários cadastrados
    all_users = db.child("usuarios").get().val()
    
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
                # Adicione os outros campos conforme necessário
            })
            flash('Dados atualizados com sucesso!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')

    return render_template('edit_user.html', user=user_data, user_id=user_id)

@admin_routes.route('/admin/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        # Excluir o usuário do banco de dados
        db.child("usuarios").child(user_id).remove()
        flash('Usuário excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir usuário: {str(e)}', 'danger')

    return redirect(url_for('admin.admin_dashboard'))
