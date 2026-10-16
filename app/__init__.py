from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

# Database Instance Initialization
db = SQLAlchemy()

# Initialization of CORS instance
cors = CORS()

# Migrate helps flask to manage database migrations. It allows you to make changes to the database schema over time without losing data. 
migrate = Migrate()

ALLOWED_HOSTS = ['https://localhost:3000']

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    print('secret key : ', os.getenv('SECRET_KEY'))

    # Configuring CORS for all the request from the domains in the ALLOWED_HOSTS list
    cors.init_app(app, resources={r'/*':{'origins': ALLOWED_HOSTS}})

    db.init_app(app)

    # Migrate app initialization
    migrate.init_app(app, db)

    import app.models as models

    #  Blueprint registration
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.blog import blog_bp
    from app.routes import general_bp

    app.register_blueprint(general_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(blog_bp)

    return app
