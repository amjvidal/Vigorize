from flask import Blueprint, render_template, request, redirect,url_for, flash, session
import json
from firebaseAuth import  atualiza_perfilfb, getUserData

perfil_routes = Blueprint('perfil', __name__)

""" Rotas de perfil
    - /perfil - Get - Retorna a página de perfil
    - /perfil/editar - PUT - Retorna a página de edição de perfil
    - /perfil/editar - POST - Edita o perfil do usuário
    - /perfil/excluir - DELETE - Exclui o perfil do usuário
"""

@perfil_routes.route('/', methods=['GET','POST'])
def pagina_perfil():
    """ Retorna a página de perfil """
    if 'user' in session:
        user_id = session['user']
        user_email = session.get('user_email')
        
        print(user_email)
        try:
            user_data = getUserData(user_email)
            return render_template('perfil.html', user_data = user_data) 
        except Exception as e:
            error_message = json.loads(e.args[1])['error']['message']
            flash(error_message, 'danger')
            return render_template('perfil.html')
    return render_template('perfil.html', user_data = user_data)
    