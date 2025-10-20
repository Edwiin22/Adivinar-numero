from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

# Variable global para almacenar el número a adivinar
import random
numero_a_adivinar = random.randint(1, 10)

# Ruta principal que redirige a /adivinar
@app.route('/')
def inicio():
    return redirect(url_for('adivinar'))

@app.route('/adivinar', methods=['GET', 'POST'])
def adivinar():
    mensaje = ''
    if request.method == 'POST':
        try:
            intento = int(request.form['numero'])
            if intento == numero_a_adivinar:
                return redirect(url_for('terminar'))
            elif intento < numero_a_adivinar:
                mensaje = 'Demasiado bajo. Intenta de nuevo.'
            else:
                mensaje = 'Demasiado alto. Intenta de nuevo.'
        except ValueError:
            mensaje = 'Por favor, ingresa un número válido.'
    return render_template('adivinar.html', mensaje=mensaje)

@app.route('/terminar')
def terminar():
    return render_template('terminar.html')

if __name__ == '__main__':
    app.run(debug=True)