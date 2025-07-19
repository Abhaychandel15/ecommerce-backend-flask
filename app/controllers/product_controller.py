from flask import jsonify
from bson import ObjectId
from app import mongo

def create_product(request):
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description', '')

    if not name or not price:
        return jsonify({"msg": "Name and price are required"}), 400

    mongo.db.products.insert_one({
        "name": name,
        "price": price,
        "description": description
    })

    return jsonify({"msg": "Product created"}), 201

def get_products():
    products = []
    for prod in mongo.db.products.find():
        prod['_id'] = str(prod['_id'])
        products.append(prod)
    return jsonify(products), 200

def update_product(request, product_id):
    data = request.get_json()
    mongo.db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": data}
    )
    return jsonify({"msg": "Product updated"}), 200

def delete_product(product_id):
    mongo.db.products.delete_one({"_id": ObjectId(product_id)})
    return jsonify({"msg": "Product deleted"}), 200
