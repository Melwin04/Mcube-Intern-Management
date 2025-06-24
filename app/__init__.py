from flask import Flask
from mongoengine import connection,connect
from models import *
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    try:
        connect(host=Config.MONGO_URI)
        if connection.get_connection():
            print("Database connected successfully.")
    except Exception as e:
        print(f"Database connection failed: {e}")

    from app.intern import internBp
    app.register_blueprint(internBp, url_prefix='/intern')
    from app.auth import authBp
    app.register_blueprint(authBp,url_prefix='/auth')

    return app
  

