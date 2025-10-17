from flask import Flask, request, session
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def nuevo_numero():
    session['numero'] = random.randint(1, 100)

def crear_html(mensaje):
    puntaje = session.get('puntaje', 0)
    return f"""
    <html>
        <body>
            <h1>Juego: Adivina el número</h1>
            <p>{mensaje}</p>
            <p>Puntaje: {puntaje}</p>
            <form method="post" action="/adivinar">
                <input type="number" name="numero" min="1" max="100" required>
                <button>Enviar intento</button>
            </form>
            <form method="post" action="/terminar">
                <button>Terminar juego</button>
            </form>
        </body>
    </html>
    """

@app.route('/')
def inicio():
    session['puntaje'] = 0
    nuevo_numero()
    return crear_html("¡Comienza el juego! Ingresa un número.")

@app.route('/adivinar', methods=['POST'])
def adivinar():
    if 'numero' not in session:
        nuevo_numero()
        session['puntaje'] = 0

    numero_objetivo = session['numero']
    puntaje = session.get('puntaje', 0)

    intento = request.form['numero']
    try:
        intento = int(intento)
    except:
        return crear_html("Por favor ingresa un número válido.")

    if intento == numero_objetivo:
        puntaje += 100
        session['puntaje'] = puntaje
        mensaje = f"¡Ganaste! El número era {numero_objetivo}. Nuevo número."
        nuevo_numero()
    else:
        mensaje = f"No, el número era {numero_objetivo}. Intenta otra vez."
        nuevo_numero()

    return crear_html(mensaje)

@app.route('/terminar', methods=['POST'])
def terminar():
    puntaje_final = session.get('puntaje', 0)
    session.clear()
    return f"""
    <html>
        <body>
            <h1>Juego terminado</h1>
            <p>Puntaje final: {puntaje_final}</p>
            <a href="/">Jugar otra vez</a>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run()