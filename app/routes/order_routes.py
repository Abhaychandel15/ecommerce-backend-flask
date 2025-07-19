from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.order_controller import place_order,view_order

order_bp = Blueprint('order', __name__)

@order_bp.route('/place', methods=['POST'])
@jwt_required()
def order_place():
    return place_order()

@order_bp.route('/history', method=['GET'])
@jwt_required()
def order_history():
    return view_order()


