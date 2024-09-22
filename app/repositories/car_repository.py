from app.models.car import Car
from app.database import get_db


class CarRepository:
    def __init__(self):
        self.db = next(get_db())

    def find_all(self):
        return self.db.query(Car).filter(Car.deleted_at == None).all()

    def find_by_id(self, car_id):
        return self.db.query(Car).filter(Car.id == car_id, Car.deleted_at == None).first()

    def find_by_owner_id(self, owner_id):
        return self.db.query(Car).filter(Car.owner_id == owner_id, Car.deleted_at == None).all()

    def create(self, car):
        self.db.add(car)
        self.db.commit()
        return car

    def update(self, car):
        self.db.commit()
        return car

    def soft_delete(self, car):
        car.deleted_at = datetime.utcnow()
        self.db.commit()
