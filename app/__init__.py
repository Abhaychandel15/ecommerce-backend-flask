from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Extensions
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    load_dotenv()  # Load from .env
    app = Flask(__name__)

    # Configuration
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix="/api/products")
    from app.routes.cart_routes import cart_bp
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    from app.routes.order_routes import order_bp
    app.register_blueprint(order_bp , url_prefix="/api/order")
    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    

    return app
