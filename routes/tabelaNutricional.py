from flask import Blueprint, render_template, request, flash, redirect, url_for
import json

tabelaNutricao = Blueprint('tabelaNutricional', __name__)

with open("dados.json",encoding="utf-8") as alimentos:
    dados=json.load(alimentos)

inflated_buttons = []

@tabelaNutricao.route('/', methods=['GET','POST'])
def tabelaNutri():  
    input=[{'id':'barraPesquisa', 'type':'text', 'placeholder':'Busque seu alimento: ','layout':'inline' }]
    if request.method=='POST':
        selected_item = request.form.get('item')
        if selected_item:
            inflated_buttons.append(selected_item)

    return render_template('tabelaNutricional.html',items=dados,buttons=inflated_buttons)


# umidade (%) - Energia (kcal) - proteina (g) gorduraTotal(g) - carboidratos (g) - FibraAlimentar(g) medidas por 100g


def getCategory(description):
    for item in dados:
        if item["description"] == description:
            return item["category"]
    return None  
