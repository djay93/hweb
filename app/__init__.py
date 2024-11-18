from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from .config import Config
from .extensions import db, migrate
from app.utils import logging_util
from flask.cli import with_appcontext
from flask_wtf.csrf import CSRFProtect, CSRFError
import click

from app.routes.workflows import workflow_bp, workflow_api_bp
from app.routes.home import home_bp
from app.routes.hmda import hmda_bp, hmda_api_bp
from app.routes.user import user_bp
from app.utils.context_processors import ContextProcessors

# Initialize CSRF protection
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Load environment configuration
    load_dotenv()
    app.config.from_object(Config)
    app.jinja_env.globals.update(max=max, min=min)
    
    
    # Initialize database and migrate extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Register blueprints
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(workflow_bp, url_prefix='/workflows')
    app.register_blueprint(hmda_bp, url_prefix='/hmda')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(workflow_api_bp, url_prefix='/api/workflows')
    app.register_blueprint(hmda_api_bp, url_prefix='/api/hmda')
    
    # Context processor
    app.context_processor(ContextProcessors.inject_nav_items)

    # Configure logging
    if not app.debug and not app.testing:
        logging_util.setup_logging(app)

    # Seed database using CLI
    @app.cli.command("seed-db")
    @with_appcontext
    def seed_db():
        """Seed the database with initial data."""
        from app.seeds.seed_data import seed_database
        seed_database()
        click.echo('Database seeded successfully!')
    
    @app.cli.command("run-huey")
    @with_appcontext
    def run_huey():
        """Run Huey consumer."""
        from app.utils.huey_config import huey
        from huey.consumer import Consumer
        
        consumer = Consumer(huey)
        consumer.run()

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        client_token = request.headers.get("X-CSRFToken")  # Or use the header name you are sending
        app.logger.error(f"CSRF validation failed. Client token: {client_token}")
        app.logger.error(f"CSRF Error: {e}")
        return jsonify({"error": "Invalid CSRF token"}), 400

    return app
