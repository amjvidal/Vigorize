from flask import Blueprint, render_template, request, redirect,url_for, flash
import json
from firebaseAuth import  atualiza_perfilfb
perfil_routes = Blueprint('perfil', __name__)

""" Rotas de perfil
    - /perfil - Get - Retorna a página de perfil
    - /perfil/editar - PUT - Retorna a página de edição de perfil
    - /perfil/editar - POST - Edita o perfil do usuário
    - /perfil/excluir - DELETE - Exclui o perfil do usuário
"""

@perfil_routes.route('/')
def pagina_perfil():
    """ Retorna a página de perfil """
    
    def inputs_perfil():
        imputs = [
            {'id': 'nome', 'type': 'text', 'placeholder': 'Nome', 'name': 'nome'},
            {'id': 'email', 'type': 'email', 'placeholder': 'Email', 'name': 'email'},
            {'id': 'senha', 'type': 'password', 'placeholder': 'Senha', 'name': 'senha'}
        ]
        if request.method == 'POST':
            data = request.form
        try:
            atualiza_perfilfb(data['nome'], data['email'], data['senha'])  # tem que fazer essa função
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('perfil.perfil'))
        except Exception as e:
            error_message = json.loads(e.args[1])['error']['message']
            flash(error_message, 'danger')
            return render_template('perfil.html', inputs=inputs_perfil())

    return render_template('perfil.html', inputs=inputs_perfil())
    