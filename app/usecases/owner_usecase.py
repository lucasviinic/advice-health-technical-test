from app.repositories.owner_repository import OwnerRepository
from app.models.owner import Owner


class OwnerUseCase:
    def __init__(self):
        self.owner_repo = OwnerRepository()

    def list_owners(self, sales_opportunity=None):
        return self.owner_repo.find_all(sales_opportunity)

    def create_owner(self, data):
        existing_owner = self.owner_repo.find_by_cpf(data['cpf'])

        if existing_owner:
            if existing_owner.deleted_at is None:
                raise ValueError(f"Owner with CPF {data['cpf']} already exists.")
            else:
                existing_owner.deleted_at = None
                updated_owner = self.owner_repo.update(existing_owner)
                return updated_owner

        new_owner = Owner(
            name=data['name'],
            cpf=data['cpf'],
            sales_opportunity=data.get('sales_opportunity', True)
        )
        return self.owner_repo.create(new_owner)

    def update_owner(self, owner_id, data):
        owner = self.owner_repo.find_by_id(owner_id)
        if not owner:
            return None

        owner.name = data.get('name', owner.name)
        owner.cpf = data.get('cpf', owner.cpf)
        owner.sales_opportunity = data.get('sales_opportunity', owner.sales_opportunity)
        
        return self.owner_repo.update(owner)

    def delete_owner(self, owner_id):
        owner = self.owner_repo.find_by_id(owner_id)
        if not owner:
            return None
        self.owner_repo.soft_delete(owner)
        return owner
