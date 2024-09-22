import uuid
import pytest
from flask import Flask
from app.routes.owner_routes import owner_bp
from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(owner_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_owners(client):
    with patch('app.usecases.owner_usecase.OwnerUseCase.list_owners',
                return_value=[MagicMock(to_dict=MagicMock(return_value={"id": "owner1"}))]):
        response = client.get('/owners')
        assert response.status_code == 200
        assert response.json == [{"id": "owner1"}]

def test_create_owner_success(client):
    owner_data = {"name": "John Doe", "cpf": "12345678900"}
    
    with patch('app.usecases.owner_usecase.OwnerUseCase.create_owner',
               return_value=MagicMock(to_dict=MagicMock(return_value={"id": "new_owner"}))):
        response = client.post('/owners', json=owner_data)
        assert response.status_code == 201
        assert response.json == {"id": "new_owner"}

def test_create_owner_error(client):
    owner_data = {"name": "John Doe"}

    with patch('app.usecases.owner_usecase.OwnerUseCase.create_owner', side_effect=Exception("Database error")):
        response = client.post('/owners', json=owner_data)
        assert response.status_code == 500
        assert "An error occurred while creating the owner" in response.json['error']

def test_update_owner_success(client):
    owner_id = uuid.uuid4()
    owner_data = {"name": "Jane Doe", "cpf": "12345678901"}

    with patch('app.usecases.owner_usecase.OwnerUseCase.update_owner',
               return_value=MagicMock(to_dict=MagicMock(return_value={"id": owner_id}))):
        response = client.put(f'/owners/{owner_id}', json=owner_data)
        assert response.status_code == 200
        assert response.json == {"id": str(owner_id)}

def test_update_owner_not_found(client):
    owner_id = uuid.uuid4()
    owner_data = {"name": "Jane Doe"}

    with patch('app.usecases.owner_usecase.OwnerUseCase.update_owner', return_value=None):
        response = client.put(f'/owners/{owner_id}', json=owner_data)
        assert response.status_code == 404
        assert response.json == {"error": "Owner not found"}

def test_delete_owner_success(client):
    owner_id = uuid.uuid4()

    with patch('app.usecases.owner_usecase.OwnerUseCase.delete_owner',
               return_value=MagicMock(to_dict=MagicMock(return_value={"id": owner_id}))):
        response = client.delete(f'/owners/{owner_id}')
        assert response.status_code == 200
        assert response.json == {"message": "Owner deleted successfully"}

def test_delete_owner_not_found(client):
    owner_id = uuid.uuid4()

    with patch('app.usecases.owner_usecase.OwnerUseCase.delete_owner', return_value=None):
        response = client.delete(f'/owners/{owner_id}')
        assert response.status_code == 404
        assert response.json == {"error": "Owner not found"}
