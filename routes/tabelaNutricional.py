from flask import Blueprint, render_template, request, flash, redirect, url_for



#falta trazer o json TACO
alimentos=[]

tabelaNutricao = Blueprint('tabelaNutri', __name__)

@tabelaNutricao.route('/', methods=['GET'])
def tabelaNutri():  
    input=[

    ]

    return render_template('tabelaNutricional.html')


# umidade (%) - Energia (kcal) - proteina (g) gorduraTotal(g) - carboidratos (g) - FibraAlimentar(g) medidas por 100g



def gordurasTotal(caloria,proteina,carboidratos):
    gordurasTotal = (caloria-(proteina*4)-(carboidratos*4))/9
    return round(gordurasTotal,2)

def getClasse(nome):
    
    return 

    

def excluiCru(nome):
    if not'Salmão' in nome:
        if 'cru' in nome:
            return None
        else:
            return nome
    else:
        return nome



