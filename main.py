from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/recuperar")
def recuperar():
    return render_template('recuperar.html')

@app.route("/cadastro")
def registro():
    return render_template('cadastro.html')

app.run(debug=True)