from flask import Blueprint, render_template, request, flash
from firebaseAuth import recoverPassword, auth
import json



perfil_routes = Blueprint('perfil', __name__)

""" Rotas de perfil
    - /perfil - Get - Retorna a página de perfil
    - /perfil/editar - PUT - Retorna a página de edição de perfil
    - /perfil/editar - POST - Edita o perfil do usuário
    - /perfil/excluir - DELETE - Exclui o perfil do usuário
"""

@perfil_routes.route('/', methods=['GET','PUT','DELETE','POST'])
def pagina_perfil():

    inputs = [
        {'id': 'nome', 'type': 'text', 'placeholder': 'Nome', 'name': 'nome'},
        {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
    ]
    if request.method == 'PUT':
        data = request.form
        try:
            # Editar perfil
            pass
        except Exception as e:
            # Captura a exceção e imprime a mensagem de erro
            error_message = json.loads(e.args[1])['error']['message']
            flash(error_message, 'danger')
            return render_template('perfil.html', inputs=inputs)
    elif request.method == 'DELETE':
        try:
            # Excluir perfil
            pass
        except Exception as e:
            # Captura a exceção e imprime a mensagem de erro
            error_message = json.loads(e.args[1])['error']['message']
            flash(error_message, 'danger')
            return render_template('perfil.html', inputs=inputs)
    elif request.method == 'POST':
        try:
            # Editar perfil
            recoverPassword(data["email"])
            flash('Email de recuperação de senha enviado!', 'success')
        except Exception as e:
            print(e)
            # Captura a exceção e imprime a mensagem de erro
            # error_message = json.loads(e.args[1])['error']['message']
            # flash(error_message, 'danger')
            # return render_template('perfil.html', inputs=inputs)
    return render_template('perfil.html', inputs=inputs)