import logging
import os
from logging.handlers import TimedRotatingFileHandler

def configure_logging(app, log_name: str = 'app.log') -> None:
    """
    Configure logging for the application with both file and stdout handlers.
    
    Args:
        app: Flask application instance
        log_name: Name of the log file
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
    root_logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplication
    if app.debug:
        root_logger.setLevel(logging.DEBUG)
    
    # Always log to stdout in production
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    root_logger.addHandler(stream_handler)

    # File logging configuration
    if not app.debug and not app.testing:
        # Time-based rotation (daily) with size limit
        file_handler = TimedRotatingFileHandler(
            filename=f'logs/{log_name}',
            when='midnight',
            interval=1,
            backupCount=30,  # Keep month worth of logs
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
