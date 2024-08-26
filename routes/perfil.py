from flask import Blueprint, render_template

perfil_routes = Blueprint('perfil', __name__)

""" Rotas de perfil
    - /perfil - Get - Retorna a página de perfil
"""

@perfil_routes.route('/')
def pagina_perfil():
    """ Retorna a página de perfil """
    return render_template('perfil.html')