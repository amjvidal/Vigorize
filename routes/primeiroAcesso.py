from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import loginfb, auth, db, emailDb, enviarDadosDb

primeiroAcesso_routes = Blueprint('primeiroAcesso',__name__)

""" Rotas de primeiroAcesso
    - /primeiroAcesso - Get - Retorna a página de perfil
    - /primeiroAcesso - Post - Salva as opções do usuário no db
"""

@primeiroAcesso_routes.route('/', methods=['GET', 'POST'])
def primeiroAcesso():
    """ Retorna a página de primeiroAcesso """
    
    user = auth.current_user
    user_email = emailDb(user['email'])
    
    generos = ["Masculino", "Feminino"]
    fisicos = ["Sedentário", "Atividade Ligeira", "Atividade Moderada", "Atividade Intensa", "Atividade Muito Intensa"]
    inputs = [
        {'id': 'altura', 'type': 'number', 'placeholder': 'Altura (em cm)', 'name': 'altura'},
        {'id': 'peso', 'type': 'number', 'placeholder': 'Peso (em kg)', 'name': 'peso'},
    ]
    if request.method == 'POST':
        data = request.form
        
        altura = data['altura']
        peso = data['peso']
        genero = data['genero']
        fisico = data['fisico']
        try:
            enviarDadosDb(user_email,altura,peso,genero,fisico)
            flash("Dados Enviados")
            return redirect(url_for('primeiroAcesso.primeiroAcesso'))
        except Exception as e:
            flash("Dados não foram enviados")
            return redirect(url_for('primeiroAcesso.primeiroAcesso'))
        
        
    
    return render_template('primeiroAcesso.html', inputs = inputs, generos = generos, fisicos = fisicos)