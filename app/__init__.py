from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# Migrate helps flask to manage database migrations. It allows you to make changes to the database schema over time without losing data. 
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'your_secret_key_here'

    db.init_app(app)
    migrate.init_app(app, db)

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

