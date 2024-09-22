from flask import Blueprint, request, jsonify
from app.usecases.car_usecase import CarUseCase


car_bp = Blueprint('cars', __name__)
car_usecase = CarUseCase()

@car_bp.route('/cars', methods=['GET'])
def get_cars():
    cars = car_usecase.list_cars()
    return jsonify([car.to_dict() for car in cars])

@car_bp.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    new_car, error = car_usecase.create_car(data)

    if error:
        return jsonify({"error": error}), 400
    return jsonify(new_car.to_dict()), 201

@car_bp.route('/cars/<uuid:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    updated_car = car_usecase.update_car(car_id, data)

    if updated_car:
        return jsonify(updated_car.to_dict())
    else:
        return jsonify({"error": "Car not found"}), 404

@car_bp.route('/cars/<uuid:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = car_usecase.delete_car(car_id)

    if car:
        return jsonify({"message": "Car deleted successfully"}), 200
    else:
        return jsonify({"error": "Car not found"}), 404
