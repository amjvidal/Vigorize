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

    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    user_email = emailDb(user['email'])
    
    generos = ["Masculino", "Feminino"]
    fisicos = ["Sedentário", "Ligeira", "Moderada", "Intensa", "Muito Intensa"]
    inputs = [

        {'id': 'altura', 'type': 'number', 'placeholder': "Altura(cm)" ,'name': 'altura','max': '250','min': '100'},
        {'id': 'peso', 'type': 'number', 'placeholder': "Peso(kg)",'name': 'peso','max': '200','min': '30'}
    ]
    if request.method == 'POST':
        data = request.form
        
        altura = int(data['altura'])
        peso = int(data['peso'])
        genero = data['genero']
        fisico = data['fisico']
        
        # if altura > 260 or altura < 50:
        #     flash("A altura é invalida!", 'danger')
        #     return redirect(url_for('primeiroAcesso.primeiroAcesso'))
        # if peso > 200 or peso < 0:
        #     flash("O peso é invalido!", 'danger')
        #     return redirect(url_for('primeiroAcesso.primeiroAcesso'))
        
        try:
            enviarDadosDb(user_email,altura,peso,genero,fisico)
            flash("Dados Enviados!", 'sucess')
            return redirect(url_for('perGordura.pagina_perGordura'))
        except Exception as e:
            flash("Dados não foram enviados!", 'danger')
            return redirect(url_for('primeiroAcesso.primeiroAcesso'))
    
    return render_template('primeiroAcesso.html', inputs = inputs, generos = generos, fisicos = fisicos)