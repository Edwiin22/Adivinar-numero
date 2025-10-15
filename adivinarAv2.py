from flask import Flask, request, session
import random

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

def iniciar_juego():
    session['numero_a_adivinar'] = random.randint(1, 100)

def crear_html(mensaje):
    return f"""
    <html>
        <head><title>Juego de Adivinar el Número</title></head>
        <body>
            <h1>¡Adivina el número entre 1 y 100!</h1>
            <p>{mensaje}</p>
            <form method="post" action="/adivinar">
                <input type="number" name="adivina" min="1" max="100" required>
                <button type="submit">Intentar</button>
            </form>
            <form method="post" action="/terminar">
                <button type="submit">Terminar juego</button>
            </form>
        </body>
    </html>
    """

@app.route('/', methods=['GET'])
def index():
    iniciar_juego()
    mensaje = "¡Nuevo juego iniciado! Ingresa tu número."
    return crear_html(mensaje)

@app.route('/adivinar', methods=['POST'])
def adivinar():
    if 'numero_a_adivinar' not in session:
        iniciar_juego()

    numero_a_adivinar = session['numero_a_adivinar']

    try:
        intento_usuario = int(request.form['adivina'])
    except ValueError:
        mensaje = "Por favor ingresa un número válido."
        return crear_html(mensaje)

    if intento_usuario == numero_a_adivinar:
        mensaje = f"¡Felicidades! Adivinaste el número {numero_a_adivinar}. Se ha generado un nuevo número para seguir jugando."
    else:
        mensaje = f"No acertaste. El número era {numero_a_adivinar}. Se ha generado un nuevo número, intenta nuevamente."

    # Generar nuevo número para la siguiente ronda
    iniciar_juego()

    return crear_html(mensaje)

@app.route('/terminar', methods=['POST'])
def terminar():
    session.clear()
    mensaje = "¡Juego terminado! Gracias por jugar."
    return crear_html(mensaje)

if __name__ == '__main__':
    app.run(debug=True)
