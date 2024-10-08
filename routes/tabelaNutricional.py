from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import json
from firebaseAuth import auth2, db, emailDb

tabelaNutricao = Blueprint('tabelaNutricional', __name__)

with open("dados.json", encoding="utf-8") as alimentos:
    dados = json.load(alimentos)

@tabelaNutricao.route('/', methods=['GET', 'POST'])
def tabelaNutri():
    user = auth2.current_user
    
    if user is None:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    try:
        user_id = emailDb(user['email'])
        profile_picture_url = db.child('usuarios').child(user_id).child('profilePicture').get().val()
        listaAlimento = db.child('usuarios').child(user_id).child('Alimentos').get()

        
        
        if listaAlimento.val() is None:
            session['inflated_buttons'] = []
        else:
            session['inflated_buttons'] = listaAlimento.val()

        if request.method == 'POST':
            data = request.form
            action = request.form.get('action')
            if action == 'pesquisa':
                selected_item = request.form.get('item')
                if selected_item not in session['inflated_buttons']:
                    session['inflated_buttons'].append(selected_item)
                    session.modified = True  
                    enviaData(user_id, session['inflated_buttons'])
            elif action == "delete_alimento":
                if 'delete_button' in request.form:
                    item_to_delete = request.form.get('delete_button')
                    eliminaAtributo(item_to_delete,session['inflated_buttons'])
                    enviaData(user_id, session['inflated_buttons'])
                    
        total_calorias = round(somaAtributo('Caloria'),2)
        total_Carboidrato = round(somaAtributo('Carboidrato'),2)
        total_Umidade = round(somaAtributo('Umidade'),2)
        total_gorduraTotal = round(somaAtributo('gorduraTotal'),2)
        total_Sodio = round(somaAtributo('Sodio'),2)
        total_proteina = round(somaAtributo('Proteína'))
        
    except Exception as e:
        error_message = str(e)
        print(error_message)
        flash('Erro ao carregar a página de tabela nutricional', 'danger')
        return redirect(url_for('login.pagina_login'))
    
    return render_template('tabelaNutricional.html', items=dados,total_Umidade=total_Umidade,total_Sodio=total_Sodio, 
    buttons=session.get('inflated_buttons', []),total_calorias=total_calorias,total_Carboidrato=total_Carboidrato,
    total_gorduraTotal=total_gorduraTotal, total_proteina=total_proteina, profile_picture_url=profile_picture_url)


def pegaAtributo(nome_alimento, atributo):
    try:
      
        for alimento in dados:
            if alimento.get('Nome') == nome_alimento:

                return alimento.get(atributo)

        print('Alimento não encontrado.')
        return None
    except Exception as e:
        error_message = str(e)
        print(error_message)
        flash('Erro ao buscar o alimento', 'danger')
        return None

def eliminaAtributo(itemElimindado,array):
    try:
        i=0
        for alimento in array:
            if alimento==itemElimindado:
                print(i)
                array.pop(i)
                return array
            i=i+1
        
    except Exception as e:
        error_message = str(e)
        print(error_message)
        flash('Erro ao deletar o alimento', 'danger')
        return None


def somaAtributo(atributo):
    totalAtributo = 0
    try:
        for nome_alimento in session.get('inflated_buttons', []):
            proteina = pegaAtributo(nome_alimento,atributo)
            if proteina is not None:
                totalAtributo += proteina
    except Exception as e:
        error_meessage = str(e)
        print(error_meessage)
        flash('Erro ao calcular a soma das proteínas', 'danger')
    
    return totalAtributo


def enviaData(user, data):
    db.child('usuarios').child(user).child('Alimentos').set(data)


