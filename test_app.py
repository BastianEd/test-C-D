"""!
@file test_app.py
@brief Pruebas unitarias para validar los endpoints de app.py.
"""

import unittest
from app import app


class TestApp(unittest.TestCase):
    """! Clase de pruebas unitarias para la aplicación Flask."""

    def setUp(self):
        """! Inicializa el cliente de pruebas de Flask."""
        self.client = app.test_client()

    def test_index(self):
        """! Verifica que la ruta raíz responda HTTP 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_hello_xss_escaped(self):
        """! Verifica el saludo y el escape de etiquetas HTML."""
        response = self.client.get('/hello?name=<script>alert(1)</script>')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<script>', response.data)


if __name__ == '__main__':
    unittest.main()
