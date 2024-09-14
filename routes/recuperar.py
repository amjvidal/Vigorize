from flask import Blueprint, render_template, request, redirect,url_for, flash
from firebaseAuth import recoverPassword
import json

recuperar_routes = Blueprint('recuperar', __name__)

""" Rotas de recuperação de senha
    - /recuperar - Get - Retorna a página de recuperação de senha
    - /recuperar - Post - Envia um email de recuperação de senha
    - /recuperar/<id_usuario>/trocarSenha - Get - Retorna a página de troca de senha
    - /recuperar/<id_usuario>/trocarSenha - Post - Troca a senha do usuário
"""

@recuperar_routes.route('/', methods=['GET','POST'])
def pagina_recuperar():
    """ Retorna a página de recuperação de senha """
    # Define os inputs da página de recuperação de senha
    inputs = [
        {'id': 'nome', 'type': 'email', 'placeholder': 'Digite seu email','name':'email'}
    ]

    if request.method == 'POST':
        data = request.form
        try:
            recoverPassword(data["email"])
            flash('Email de recuperação de senha enviado!', 'success')
            return render_template('recuperar.html', inputs=inputs)
        
        except Exception as e:
            error_message = str(e)
            print(error_message)
            flash('Erro ao enviar email de recuperação de senha!', 'danger')
            return render_template('recuperar.html', inputs=inputs)
        
    return render_template('recuperar.html', inputs=inputs)