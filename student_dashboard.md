import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.maintenance import maintenance_bp
    from app.routes.admin import admin_bp
    from app.routes.shared import shared_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(shared_bp)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Ensure instance folder exists
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance'), exist_ok=True)

    # Create database tables
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    # Context processor for unread notification count
    @app.context_processor
    def inject_notification_count():
        from flask_login import current_user
        if current_user.is_authenticated:
            from app.utils.notifications import get_unread_count
            return dict(unread_notification_count=get_unread_count(current_user.id))
        return dict(unread_notification_count=0)

    return app
