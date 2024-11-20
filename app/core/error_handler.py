import logging
import json
from typing import Any, Dict, Optional
from .exceptions import ApplicationError, ErrorCode

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.exception_mapping = {
            FileNotFoundError: ErrorCode.FILE_NOT_FOUND,
            PermissionError: ErrorCode.FILE_ACCESS_DENIED,
            TimeoutError: ErrorCode.TIMEOUT_ERROR
            # Add more exceptions here
        }

    def handle_error(
        self,
        error: Exception,
        source_type: Optional[str] = None,
        source_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ApplicationError:
        """Convert any error to ApplicationError and handle logging"""
        
        if isinstance(error, ApplicationError):
            app_error = error
        else:
            error_code = self.exception_mapping.get(type(error), ErrorCode.UNEXPECTED_ERROR)
            app_error = ApplicationError(
                code=error_code,
                message=str(error),
                details=context,
                original_error=error
            )

        # Enhance error details with context
        error_details = {
            **(app_error.details or {}),
            **(context or {}),
            f"{source_type}": source_id
        }
        
        # Log the error as a JSON string
        self.log_error(app_error, error_details)
        return app_error

    def log_error(self, app_error: ApplicationError, details: Dict[str, Any]) -> None:
        """Log errors in a structured format"""
        error_message = {
            "timestamp": logging.Formatter().formatTime(logging.LogRecord(None, None, None, None, None, None, None)),
            "error_code": app_error.code.value,
            "error_type": app_error.code.name,
            "message": app_error.message,
            "details": details,
            "original_error": str(app_error.original_error) if app_error.original_error else None
        }
        self.logger.error(json.dumps(error_message, indent=2))
