from datetime import datetime, timezone
from app.models.owner import Owner
from app.database import get_db


class OwnerRepository:
    def __init__(self):
        self.db = next(get_db())

    def find_all(self, sales_opportunity=None):
        query = self.db.query(Owner).filter(Owner.deleted_at == None)
        if sales_opportunity is not None:
            query = query.filter(Owner.sales_opportunity == sales_opportunity)
        return query.all()

    def find_by_id(self, owner_id):
        return self.db.query(Owner).filter(Owner.id == owner_id, Owner.deleted_at == None).first()
    
    def find_by_cpf(self, cpf):
        return self.db.query(Owner).filter(Owner.cpf == cpf, Owner.deleted_at == None).first()

    def create(self, owner):
        self.db.add(owner)
        self.db.commit()
        return owner

    def update(self, owner):
        self.db.commit()
        return owner

    def soft_delete(self, owner):
        owner.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
