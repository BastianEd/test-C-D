from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return "Aplicación de ejemplo para gestión de dependencias - Guía 3.3.2"

@app.route('/hello')
def hello():
    name = escape(request.args.get('name', 'Invitado'))
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
