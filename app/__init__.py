from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from .config import Config
from .extensions import db, migrate
from logging.handlers import RotatingFileHandler
from app.utils import logging_util

from app.routes.workflows import workflow_bp
from app.routes.dashboard import dashboard_bp
from app.routes.hmda import hmda_bp


def create_app():
    app = Flask(__name__)

    # Load environment configuration
    load_dotenv()
    app.config.from_object(Config)
    
    # Initialize database and migrate extensions
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(workflow_bp, url_prefix='/workflows')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(hmda_bp, url_prefix='/hmda')
    
    @app.route('/')
    def home():
        return "EC Workflow Automation is up and running."

    if not app.debug and not app.testing:
        logging_util.configure_logging(app)

    return app
