from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import auth, db, emailDb

loginadmin_routes = Blueprint('loginadmin', __name__)

@loginadmin_routes.route('/', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        try:
            # Autenticação do administrador no Firebase
            admin_user = auth.sign_in_with_email_and_password(email, senha)
            user_info = auth.get_account_info(admin_user['idToken'])

            # Verifica se o usuário é um administrador no banco de dados
            user_id = emailDb(email)
            user_data = db.child("usuarios").child(user_id).get().val()

            if user_data and user_data.get('is_admin'):
                flash('Login de administrador bem-sucedido!', 'success')
                return redirect(url_for('admin.admin_dashboard'))  # Redireciona para o dashboard do admin
            else:
                flash('Você não tem permissão de administrador', 'danger')
        except Exception as e:
            error_message = e.args[1] if isinstance(e.args[1], str) else e.args[1].get('error', {}).get('message', 'Erro desconhecido')
            flash(f'Erro: {error_message}', 'danger')

    return render_template('loginadmin.html')
