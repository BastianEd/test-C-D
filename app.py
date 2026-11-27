"""!
@file app.py
@brief Servicio Flask instrumentado con métricas para Prometheus (Guía 3.5.2).
@author Bastian Rubio
@version 1.0.0
"""
from flask import Flask, request, Response
from markupsafe import escape
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Definición de métricas para Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total de peticiones HTTP recibidas',
    ['method', 'endpoint']
)
REQUEST_TIME = Summary(
    'request_processing_seconds',
    'Tiempo empleado procesando la petición'
)


@app.route('/')
def index():
    """! Endpoint raíz de verificación del servicio. """
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return "Servicio Flask Monitorizado - Guía 3.5.2"


@app.route('/hello')
@REQUEST_TIME.time()
def hello():
    """! Endpoint de saludo protegido contra XSS y medido en latencia. """
    REQUEST_COUNT.labels(method='GET', endpoint='/hello').inc()
    name = escape(request.args.get('name', 'Invitado'))
    return f"Hello, {name}!"


@app.route('/metrics')
def metrics():
    """! Expone las métricas recolectadas en formato nativo de Prometheus. """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
