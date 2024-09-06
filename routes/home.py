from flask import Blueprint, render_template, request, flash, redirect, url_for

home_routes = Blueprint('home',__name__)

""" Rotas de home
    - /primeiroAcesso - Get - Retorna a página de perfil
"""
@home_routes.route('/', methods=['GET','POST'])
def home():
    """ Retorna a página de home """
    
    if request.method=='POST':
        return redirect(url_for('login.pagina_login'))
    
    return render_template('home.html')