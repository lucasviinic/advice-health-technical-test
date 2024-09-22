from app.repositories.car_repository import CarRepository
from app.repositories.owner_repository import OwnerRepository
from app.models.car import Car


class CarUseCase:
    def __init__(self):
        self.car_repo = CarRepository()
        self.owner_repo = OwnerRepository()

    def list_cars(self):
        return self.car_repo.find_all()

    def create_car(self, data):
        owner_id = data['owner_id']

        owner = self.owner_repo.find_by_id(owner_id)
        if not owner:
            return None, "Owner not found"

        car_count = len(self.car_repo.find_by_owner_id(owner_id))
        if car_count >= 3:
            return None, "Owner already has 3 cars"

        new_car = Car(
            color=data['color'],
            model=data['model'],
            owner_id=owner_id
        )
        return self.car_repo.create(new_car), None

    def update_car(self, car_id, data):
        car = self.car_repo.find_by_id(car_id)
        if not car:
            return None

        car.color = data.get('color', car.color)
        car.model = data.get('model', car.model)

        return self.car_repo.update(car)

    def delete_car(self, car_id):
        car = self.car_repo.find_by_id(car_id)
        if not car:
            return None
        self.car_repo.soft_delete(car)
        return car
