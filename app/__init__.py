import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.database import Base, engine
from app.models import car, owner

from app.routes.owner_routes import owner_bp
from app.routes.car_routes import car_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

Base.metadata.create_all(bind=engine)

app.register_blueprint(owner_bp)
app.register_blueprint(car_bp)