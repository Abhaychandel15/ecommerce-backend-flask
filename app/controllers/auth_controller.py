from flask import jsonify
from flask_jwt_extended import create_access_token
from app import mongo, bcrypt

def register_user(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role =  data.get('role','customer')

    if mongo.db.users.find_one({'username': username}):
        return jsonify({"msg": "User already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    mongo.db.users.insert_one({'username': username, 'password': hashed_pw, 'role':role})


    return jsonify({"msg": "User registered successfully"}), 201

def login_user(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({'username': username})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify({"token": token}), 200
