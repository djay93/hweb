from enum import Enum
from typing import Any, Dict, Optional

class ErrorCode(Enum):
    # System Level Errors (1000-1999)
    SYSTEM_ERROR = 1000
    UNEXPECTED_ERROR = 1001
    DATABASE_ERROR = 1002
    TIMEOUT_ERROR = 1003
    NETWORK_ERROR = 1004
    CONNECTION_TIMEOUT = 1005
    INVALID_RESPONSE = 1006
    
    # File Operation Errors (2000-2999)
    FILE_NOT_FOUND = 2000
    FILE_ACCESS_DENIED = 2001
    FILE_CORRUPTED = 2002
    
    # Application Specific Errors (4000-4999)
    HMDA_VALIDATION_ERROR = 4000
    HMDA_MISSING_REQUIRED_FIELDS = 4001
    HMDA_BAD_DATA_FORMAT = 4002

class ApplicationError(Exception):
    def __init__(
        self, 
        code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        self.original_error = original_error
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_code": self.code.value,
            "error_type": self.code.name,
            "message": self.message,
            "details": self.details
        }