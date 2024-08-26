from flask import Blueprint, render_template, request, flash, redirect, url_for

primeiroAcesso_routes = Blueprint('primeiroAcesso',__name__)

""" Rotas de primeiroAcesso
    - /primeiroAcesso - Get - Retorna a página de perfil
    - /primeiroAcesso - Post - Salva as opções do usuário no db
"""

@primeiroAcesso_routes.route('/', methods=['GET', 'POST'])
def primeiroAcesso():
    """ Retorna a página de primeiroAcesso """
    
    return render_template('primeiroAcesso.html')