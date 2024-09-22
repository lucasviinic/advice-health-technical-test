import uuid
import pytest
from flask import Flask
from app.routes.car_routes import car_bp
from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(car_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_cars(client):
    with patch('app.usecases.car_usecase.CarUseCase.list_cars', \
                return_value=[MagicMock(to_dict=MagicMock(return_value={"id": "car1"}))]):
        response = client.get('/cars')
        assert response.status_code == 200
        assert response.json == [{"id": "car1"}]

def test_create_car_success(client):
    car_data = {"color": "blue", "model": "sedan", "owner_id": "owner_id"}
    
    with patch('app.usecases.car_usecase.CarUseCase.create_car', \
               return_value=(MagicMock(to_dict=MagicMock(return_value={"id": "new_car"})), None)):
        response = client.post('/cars', json=car_data)
        assert response.status_code == 201
        assert response.json == {"id": "new_car"}

def test_create_car_owner_not_found(client):
    car_data = {"color": "blue", "model": "sedan", "owner_id": "unknown_owner"}
    
    with patch('app.usecases.car_usecase.CarUseCase.create_car', return_value=(None, "Owner not found")):
        response = client.post('/cars', json=car_data)
        assert response.status_code == 400
        assert response.json == {"error": "Owner not found"}

def test_update_car_success(client):
    car_id = uuid.uuid4()
    car_data = {"color": "yellow", "model": "hatch"}

    with patch('app.usecases.car_usecase.CarUseCase.update_car', \
               return_value=MagicMock(to_dict=MagicMock(return_value={"id": car_id}))):
        response = client.put(f'/cars/{car_id}', json=car_data)
        assert response.status_code == 200
        assert response.json == {"id": str(car_id)}

def test_update_car_not_found(client):
    car_id = uuid.uuid4()
    car_data = {"color": "yellow", "model": "hatch"}

    with patch('app.usecases.car_usecase.CarUseCase.update_car', return_value=None):
        response = client.put(f'/cars/{car_id}', json=car_data)
        assert response.status_code == 404
        assert response.json == {"error": "Car not found"}

def test_delete_car_success(client):
    car_id = uuid.uuid4()

    with patch('app.usecases.car_usecase.CarUseCase.delete_car', \
               return_value=MagicMock(to_dict=MagicMock(return_value={"id": car_id}))):
        response = client.delete(f'/cars/{car_id}')
        assert response.status_code == 200
        assert response.json == {"message": "Car deleted successfully"}

def test_delete_car_not_found(client):
    car_id = uuid.uuid4()

    with patch('app.usecases.car_usecase.CarUseCase.delete_car', return_value=None):
        response = client.delete(f'/cars/{car_id}')
        assert response.status_code == 404
        assert response.json == {"error": "Car not found"}
