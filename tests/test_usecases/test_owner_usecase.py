import uuid
import pytest
from unittest.mock import MagicMock
from app.usecases.owner_usecase import OwnerUseCase
from app.models.owner import Owner


@pytest.fixture
def owner_usecase():
    return OwnerUseCase()

def test_list_owners(owner_usecase):
    owner_usecase.owner_repo.find_all = MagicMock(return_value=["owner1", "owner2"])

    result = owner_usecase.list_owners()
    assert result == ["owner1", "owner2"]

def test_create_owner_success(owner_usecase):
    owner_usecase.owner_repo.create = MagicMock(return_value="new_owner")

    data = {
        "name": "John Doe",
        "cpf": "12345678900"
    }

    result = owner_usecase.create_owner(data)
    
    assert result == "new_owner"

def test_create_owner_missing_name(owner_usecase):
    data = {
        "cpf": "12345678900"
    }

    with pytest.raises(KeyError) as exc_info:
        owner_usecase.create_owner(data)

    assert "name" in str(exc_info.value)

def test_create_owner_missing_cpf(owner_usecase):
    data = {
        "name": "John Doe"
    }

    with pytest.raises(KeyError) as exc_info:
        owner_usecase.create_owner(data)

    assert "cpf" in str(exc_info.value)

def test_update_owner_success(owner_usecase):
    owner = Owner(name="Jane Doe", cpf="12345678901")
    owner_usecase.owner_repo.find_by_id = MagicMock(return_value=owner)
    owner_usecase.owner_repo.update = MagicMock(return_value=owner)

    data = {
        "name": "Jane Smith"
    }

    result = owner_usecase.update_owner(owner.id, data)
    
    assert result.name == "Jane Smith"

def test_update_owner_not_found(owner_usecase):
    owner_usecase.owner_repo.find_by_id = MagicMock(return_value=None)

    data = {
        "name": "Nonexistent Owner"
    }

    result = owner_usecase.update_owner(uuid.uuid4(), data)
    
    assert result is None

def test_delete_owner_success(owner_usecase):
    owner = Owner(name="Jane Doe", cpf="12345678901")
    owner_usecase.owner_repo.find_by_id = MagicMock(return_value=owner)
    owner_usecase.owner_repo.soft_delete = MagicMock()

    result = owner_usecase.delete_owner(owner.id)
    
    assert result == owner
    owner_usecase.owner_repo.soft_delete.assert_called_once_with(owner)

def test_delete_owner_not_found(owner_usecase):
    owner_usecase.owner_repo.find_by_id = MagicMock(return_value=None)

    result = owner_usecase.delete_owner(uuid.uuid4())
    
    assert result is None
