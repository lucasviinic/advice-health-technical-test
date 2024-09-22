import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.database import Base, engine
from app.models import car, owner
from app.routes.owner_routes import owner_bp
from app.routes.car_routes import car_bp
from app.routes.auth_routes import auth_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

Base.metadata.create_all(bind=engine)

app.register_blueprint(auth_bp)
app.register_blueprint(owner_bp)
app.register_blueprint(car_bp)

@app.before_request
def check_jwt():
    from flask import request, jsonify
    from flask_jwt_extended import verify_jwt_in_request

    public_routes = ['/login', '/register']

    if request.path not in public_routes:
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Unauthorized", "details": str(e)}), 401
