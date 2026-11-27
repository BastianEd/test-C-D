"""!
@file app.py
@brief Aplicación web Flask documentada para trazabilidad y CI/CD (Guía 3.4.2).
@author Bastian Rubio
@version 1.0.0

Rapanui
"""

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    """!
    Endpoint raíz de verificación del servicio.

    Retorna:
        str: Mensaje de estado de la aplicación.
    """
    return "API Documentada - Guía 3.4.2"


@app.route('/hello')
def hello():
    """!
    Endpoint para saludar al usuario de forma segura.

    Parámetros:
        name (str): Nombre del usuario recibido por query string.

    Retorna:
        str: Mensaje de saludo sanitizado contra XSS.
    """
    name = escape(request.args.get('name', 'Invitado'))
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
