import logging
import os
from logging.handlers import TimedRotatingFileHandler
from flask import request

def setup_logging(app, log_name: str = 'app.log', log_level=logging.INFO) -> None:
    """
    Configure logging for the application with both file and stdout handlers.
    
    Args:
        app: Flask application instance
        log_name: Name of the log file
        log_level: Default logging level
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs', exist_ok=True)

    # Set up formatter with more detailed information
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level if not app.debug else logging.DEBUG)

    # Clear existing handlers to avoid duplication
    root_logger.handlers.clear()

    # Log to stdout in all environments
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    root_logger.addHandler(stream_handler)

    # File logging for production
    if not app.debug and not app.testing:
        file_handler = TimedRotatingFileHandler(
            filename=f'logs/{app.config["ENV"]}_{log_name}',
            when='midnight',
            interval=1,
            backupCount=30,  # Keep a month’s worth of logs
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)

    # Reduce noise from third-party libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

    # Log application startup
    app.logger.info(f"Application started - Running in {app.config['ENV']} mode")

    # Add a request log for each request in production
    if not app.testing:
        @app.before_request
        def log_request_info():
            app.logger.info(f"Request: {request.method} {request.path} - From: {request.remote_addr}")
