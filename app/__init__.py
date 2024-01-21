# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
  app = Flask(__name__)

  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

  db.init_app(app)
  bcrypt.init_app(app)
  jwt.init_app(app)

  from users.routes import users_bp
  app.register_blueprint(users_bp, url_prefix='/user')  

  return app 


