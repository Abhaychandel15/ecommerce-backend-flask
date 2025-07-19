from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from app import mongo

def add_to_cart(request):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    username = get_jwt_identity()

    if not product_id:
        return jsonify({"msg": "Product ID is required"}), 400

    cart = mongo.db.carts.find_one({"username": username, "product_id": product_id})
    if cart:
        mongo.db.carts.update_one(
            {"_id": cart['_id']},
            {"$inc": {"quantity": quantity}}
        )
    else:
        mongo.db.carts.insert_one({
            "username": username,
            "product_id": product_id,
            "quantity": quantity
        })

    return jsonify({"msg": "Added to cart"}), 201

def view_cart():
    username = get_jwt_identity()
    items = list(mongo.db.carts.find({"username": username}))
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items), 200

def remove_from_cart(request):
    username = get_jwt_identity()
    product_id = request.get_json().get('product_id')
    if not product_id:
        return jsonify({"msg": "Product ID required"}), 400

    mongo.db.carts.delete_one({"username": username, "product_id": product_id})
    return jsonify({"msg": "Item removed from cart"}), 200
