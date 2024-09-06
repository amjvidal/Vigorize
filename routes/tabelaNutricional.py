from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import json
from firebaseAuth import auth, db, emailDb

tabelaNutricao = Blueprint('tabelaNutricional', __name__)

with open("dados.json", encoding="utf-8") as alimentos:
    dados = json.load(alimentos)

@tabelaNutricao.route('/', methods=['GET', 'POST'])
def tabelaNutri():
    user = auth.current_user
    
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    try:
        user_email = emailDb(user['email'])   
        listaAlimento = db.child('usuarios').child(user_email).child('Alimentos').get()
        
        if request.method == 'POST':
            if listaAlimento.val() is None:
                session['inflated_buttons'] = []
            else:
                session['inflated_buttons'] = listaAlimento.val()

            selected_item = request.form.get('item')

            if selected_item and selected_item not in session['inflated_buttons']:
                session['inflated_buttons'].append(selected_item)
                session.modified = True  
                enviaData(user_email, session['inflated_buttons'])
    
    except Exception as e:
        print(f'Erro: {e}')
        return redirect(url_for('login.pagina_login'))
    
    return render_template('tabelaNutricional.html', items=dados, buttons=session.get('inflated_buttons', []))

def enviaData(user, data):
    db.child('usuarios').child(user).child('Alimentos').set(data)


