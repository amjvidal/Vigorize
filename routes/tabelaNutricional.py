from flask import Blueprint, render_template, request, flash, redirect, url_for

tabelaNutricao = Blueprint('tabelaNutri', __name__)

@tabelaNutricao.route('/', methods=['GET'])
def tabelaNutricao():  

    return render_template('tabelaNutricional.html')

