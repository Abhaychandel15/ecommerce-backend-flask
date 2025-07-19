# Middleware – Get Current User from JWT
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import request, jsonify
from app import mongo

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = mongo.db.users.find_one({'username': current_user})
        if user and user.get('role') == 'admin':
            return fn(*args, **kwargs)
        return jsonify({"msg": "Admins only!"}), 403
    return wrapper

