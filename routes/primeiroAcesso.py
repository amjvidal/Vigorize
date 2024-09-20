from flask import Blueprint, render_template, request, flash, redirect, url_for
from firebaseAuth import loginfb, auth2, db, emailDb, enviarDadosDb, storage, img_url_firebase
from werkzeug.utils import secure_filename
import os

primeiroAcesso_routes = Blueprint('primeiroAcesso',__name__)

""" Rotas de primeiroAcesso
    - /primeiroAcesso - Get - Retorna a página de perfil
    - /primeiroAcesso - Post - Salva as opções do usuário no db
"""

@primeiroAcesso_routes.route('/', methods=['GET', 'POST'])
def primeiroAcesso():
    """ Retorna a página de primeiroAcesso """
    
    user = auth2.current_user

    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    user_id = emailDb(user['email'])
    try:
        user_data = db.child("usuarios").child(user_id).get().val()
        profile_picture_url = user_data.get('profilePicture', None)
    except:
        profile_picture_url = None
    
    generos = ["Masculino", "Feminino"]
    fisicos = ["Sedentário", "Ligeira", "Moderada", "Intensa", "Muito Intensa"]
    inputs = [

        {'id': 'altura', 'type': 'number', 'placeholder': "Altura(cm)" ,'name': 'altura','max': '250','min': '100'},
        {'id': 'peso', 'type': 'number', 'placeholder': "Peso(kg)",'name': 'peso','max': '200','min': '30'}
    ]
    if request.method == 'POST':
        data = request.form
        action = data.get('action')

        if action == 'send_data':
            
            altura = int(data['altura'])
            peso = int(data['peso'])
            genero = data['genero']
            fisico = data['fisico']

            
            try:
                from firebaseAuth import profilePics_folder

                if not os.path.exists(profilePics_folder):
                    os.makedirs(profilePics_folder)  

                if 'file' not in request.files:
                    flash('Nenhum arquivo selecionado.')
                    return redirect(url_for('primeiroAcesso.primeiroAcesso'))
                
                file = request.files['file']

                if file.filename == '':
                    flash('Nenhum arquivo selecionado.')
                    return redirect(url_for('primeiroAcesso.primeiroAcesso'))
                if file:
                    # Salva a imagem no diretório local
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(profilePics_folder, filename)
                    file.save(file_path)

                    # Salva a imagem no storage do Firebase
                    storage.child(f"profile_pics/{user_id}").put(file_path)

                    # URL da imagem
                    blob = storage.child(f"profile_pics/{user_id}/{filename}")
                    url = blob.get_url(None)
                    download_url = img_url_firebase(url)

                    # Salvar a URL no Firebase Realtime Database
                    db.child("usuarios").child(user_id).update({
                        'profilePicture': download_url
                    })
                    os.remove(file_path)
                
                
                enviarDadosDb(user_id,altura,peso,genero,fisico)
                flash("Dados Enviados!", 'sucess')
                return redirect(url_for('perGordura.pagina_perGordura'))
            
            except Exception as e:
            
                flash("Dados não foram enviados!", 'danger')
                error_message = str(e)
                print(error_message)
                flash("Erro ao salvar a imagem", 'danger')
                return redirect(url_for('primeiroAcesso.primeiroAcesso'))
    
    return render_template('primeiroAcesso.html', inputs = inputs, 
                           generos = generos, 
                           fisicos = fisicos,
                           profile_picture_url = profile_picture_url)