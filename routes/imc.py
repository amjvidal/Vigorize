from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from firebaseAuth import recoverPassword, db, auth, emailDb
import json
from calculadora import calculaIMC

imc_routes = Blueprint('imc', __name__)

@imc_routes.route('/', methods=['GET', 'POST'])
def pagina_calculadora_imc():
    imc_result = None

    if request.method == 'POST':
        try:
            altura = float(request.form.get('altura')) / 100  # Converte para metros
            peso = float(request.form.get('peso'))
            imc_result = (calculaIMC(peso, altura))/10000
            
            flash(f'Seu IMC é: {imc_result:.2f}', 'success')
        except ValueError:
            flash('Por favor, insira valores válidos para altura e peso.', 'danger')

    return render_template('calculadora_imc.html', imc_result=imc_result)
