from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.cart_controller import add_to_cart, view_cart, remove_from_cart

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_cart():
    return add_to_cart(request)

@cart_bp.route('/view', methods=['GET'])
@jwt_required()
def view_user_cart():
    return view_cart()

@cart_bp.route('/remove', methods=['DELETE'])
@jwt_required()
def remove_cart_item():
    return remove_from_cart(request)
