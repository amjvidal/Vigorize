from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import json

tabelaNutricao = Blueprint('tabelaNutricional', __name__)

with open("dados.json", encoding="utf-8") as alimentos:
    dados = json.load(alimentos)

@tabelaNutricao.route('/', methods=['GET', 'POST'])
def tabelaNutri():
    
    if 'inflated_buttons' not in session:
        session['inflated_buttons'] = []
    
    if request.method == 'POST':
        selected_item = request.form.get('item')
        if selected_item and selected_item not in session['inflated_buttons']:
           
            session['inflated_buttons'].append(selected_item)
            session.modified = True  
            
    
    return render_template('tabelaNutricional.html', items=dados, buttons=session['inflated_buttons'])
