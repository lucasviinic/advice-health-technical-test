from flask import Blueprint, request, jsonify
from app.usecases.owner_usecase import OwnerUseCase


owner_bp = Blueprint('owners', __name__)
owner_usecase = OwnerUseCase()

@owner_bp.route('/owners', methods=['GET'])
def get_owners():
    sales_opportunity = request.args.get('sales_opportunity')
    owners = owner_usecase.list_owners(sales_opportunity)
    return jsonify([owner.to_dict() for owner in owners])

@owner_bp.route('/owners', methods=['POST'])
def create_owner():
    data = request.get_json()
    new_owner = owner_usecase.create_owner(data)
    
    if new_owner:
        return jsonify(new_owner.to_dict()), 201
    else:
        return jsonify({"error": "Unable to create owner"}), 400

@owner_bp.route('/owners/<uuid:owner_id>', methods=['PUT'])
def update_owner(owner_id):
    data = request.get_json()
    updated_owner = owner_usecase.update_owner(owner_id, data)

    if updated_owner:
        return jsonify(updated_owner.to_dict())
    else:
        return jsonify({"error": "Owner not found"}), 404

@owner_bp.route('/owners/<uuid:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    owner = owner_usecase.delete_owner(owner_id)

    if owner:
        return jsonify({"message": "Owner deleted successfully"}), 200
    else:
        return jsonify({"error": "Owner not found"}), 404
