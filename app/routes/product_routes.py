from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers.product_controller import (
    create_product, get_products, update_product, delete_product
)
from app.utils.jwt_helper import admin_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def add_product():
    return create_product(request)

@product_bp.route('/', methods=['GET'])
def list_products():
    return get_products()

@product_bp.route('/<product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def edit_product(product_id):
    return update_product(request, product_id)

@product_bp.route('/<product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def remove_product(product_id):
    return delete_product(product_id)
