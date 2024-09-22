import uuid
import pytest
from unittest.mock import MagicMock
from app.usecases.car_usecase import CarUseCase


@pytest.fixture
def car_usecase():
    return CarUseCase()

def test_list_cars(car_usecase):
    car_usecase.car_repo.find_all = MagicMock(return_value=["car1", "car2"])

    result = car_usecase.list_cars()
    assert result == ["car1", "car2"]

def test_create_car_success(car_usecase):
    car_usecase.owner_repo.find_by_id = MagicMock(return_value={"id": "owner_id"})
    car_usecase.car_repo.find_by_owner_id = MagicMock(return_value=[])
    car_usecase.car_repo.create = MagicMock(return_value="new_car")

    data = {
        "color": "blue",
        "model": "sedan",
        "owner_id": "owner_id"
    }

    result, error = car_usecase.create_car(data)
    
    assert result == "new_car"
    assert error is None

def test_create_car_owner_not_found(car_usecase):
    car_usecase.owner_repo.find_by_id = MagicMock(return_value=None)

    data = {
        "color": "blue",
        "model": "sedan",
        "owner_id": "unknown_owner"
    }

    result, error = car_usecase.create_car(data)
    
    assert result is None
    assert error == "Owner not found"

def test_create_car_owner_has_too_many_cars(car_usecase):
    car_usecase.owner_repo.find_by_id = MagicMock(return_value={"id": "owner_id"})
    car_usecase.car_repo.find_by_owner_id = MagicMock(return_value=["car1", "car2", "car3"])

    data = {
        "color": "blue",
        "model": "sedan",
        "owner_id": "owner_id"
    }

    result, error = car_usecase.create_car(data)

    assert result is None
    assert error == "Owner already has 3 cars"

def test_create_car_invalid_model(car_usecase):
    car_usecase.owner_repo.find_by_id = MagicMock(return_value={"id": uuid.uuid4()})
    car_usecase.car_repo.find_by_owner_id = MagicMock(return_value=[])

    data = {
        "color": "blue",  # Valid color
        "model": "truck",  # Invalid model
        "owner_id": uuid.uuid4()
    }

    with pytest.raises(ValueError) as exc_info:
        car_usecase.create_car(data)

    assert "Invalid value for car model" in str(exc_info.value)

def test_create_car_invalid_color(car_usecase):
    car_usecase.owner_repo.find_by_id = MagicMock(return_value={"id": uuid.uuid4()})
    car_usecase.car_repo.find_by_owner_id = MagicMock(return_value=[])

    data = {
        "color": "green",  # Invalid color
        "model": "sedan",  # Valid model
        "owner_id": uuid.uuid4()
    }

    with pytest.raises(ValueError) as exc_info:
        car_usecase.create_car(data)

    assert "Invalid value for car color" in str(exc_info.value)