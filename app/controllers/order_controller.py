from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app import mongo
import datetime
from bson import ObjectId

def place_order():
    username = get_jwt_identity()
    cart_items = list(mongo.db.carts.find({"username": username}))

    if not cart_items:
        return jsonify({"msg": "Cart is empty"}), 400

    for item in cart_items:
        product = mongo.db.products.find_one({"_id": ObjectId(item["product_id"])})
        if not product:
            return jsonify({"msg": f"Product not found: {item['product_id']}"}), 404

        if product["stock"] < item["quantity"]:
            return jsonify({"msg": f"Not enough stock for {product['title']}" }), 400

        mongo.db.products.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": -item["quantity"]}}
        )

    order_data = {
        "username": username,
        "items": cart_items,
        "created_at": datetime.datetime.utcnow()
    }

    mongo.db.orders.insert_one(order_data)
    mongo.db.carts.delete_many({"username": username})

    return jsonify({"msg": "Order placed and stock updated "}), 201


def view_order():
    username = get_jwt_identity()
    orders = mongo.db.orders.find({"username":username})

    for order in orders:
        order['_id'] = str(order['_id'])
        order['created_at'] = order['created_at'].strftime('%Y-%m-%d %H:%M')
    return jsonify(orders)

