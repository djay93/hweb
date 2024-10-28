from app.extensions import db
from app.models import Workflow

class WorkflowService:
    @staticmethod
    def get_all_workflows():
        """Retrieve all workflows from the database"""
        return Workflow.query.all()

    @staticmethod
    def get_workflow_by_id(workflow_id):
        """Retrieve a specific workflow by its ID"""
        return Workflow.query.get(workflow_id)

    @staticmethod
    def create_workflow(name, description=None):
        """Create a new workflow"""
        workflow = Workflow(name=name, description=description)
        db.session.add(workflow)
        db.session.commit()
        return workflow
