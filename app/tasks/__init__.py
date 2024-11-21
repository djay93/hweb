from typing import Optional
from huey import SqliteHuey
from flask import Flask

class TaskRegistry:
    def __init__(self) -> None:
        self.huey: Optional[SqliteHuey] = None
        self.hmda_tasks = None
        self._initialized = False

    def init_app(self, app: Flask) -> None:
        """Initialize the task registry with a Flask application.
        
        Args:
            app: Flask application instance
        
        Raises:
            RuntimeError: If initialization fails
        """
        try:
            self.huey = SqliteHuey(
                filename=app.config.get('HUEY_DB_PATH', "instance/ec_workflows.db"),
                immediate=False
            )
            
            # Import task classes after huey is ready
            from .hmda_tasks import HmdaTasks
            self.hmda_tasks = HmdaTasks(self.huey)
            self._initialized = True
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize TaskRegistry: {str(e)}")
        
# Create a single instance
tasks = TaskRegistry()