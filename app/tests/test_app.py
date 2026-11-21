import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app


def test_health_check():
    client = app.test_client()
    response = client.get('/')
    data = response.get_json()
    assert response.status_code == 200
    assert data["estado"] == "OK"


def test_crear_mensaje_sin_contenido():
    client = app.test_client()
    response = client.post('/mensajes', json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


@patch('app.get_db_connection')
def test_crear_mensaje_exitoso(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "2026-11-21 10:00:00")
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    client = app.test_client()
    response = client.post('/mensajes', json={"contenido": "Prueba CI con Jenkins"})
    data = response.get_json()

    assert response.status_code == 201
    assert data["estado"] == "Guardado exitosamente"
    assert data["id"] == 1


@patch('app.get_db_connection')
def test_listar_mensajes(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "Mensaje 1", "2026-11-21 10:00:00")]
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    client = app.test_client()
    response = client.get('/mensajes')
    data = response.get_json()

    assert response.status_code == 200
    assert data["total"] == 1