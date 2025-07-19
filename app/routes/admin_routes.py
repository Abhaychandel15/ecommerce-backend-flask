from flask import Blueprint,jsonify
from flask_jwt_extended import get_jwt_identity,jwt_required
from app import mongo

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def view_all_orders():
    username = get_jwt_identity()
    current_user = mongo.db.users.find_one({"username":username})
    
    if not current_user or current_user.get("role")!= "admin":
        return jsonify({"msg":"for admin access only"}),403
    
    orders = list(mongo.db.orders.find())
    for order in orders:
        order["_id"] = str(order["_id"])
        order["created_at"] = order["created_at"].strftime("%Y-%m-%d %H:%M")
    return jsonify(orders), 200