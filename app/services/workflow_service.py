from app.extensions import db
from app.models import Workflow

class WorkflowService:
    @staticmethod
    def get_workflows(page=1, per_page=10):
        """Retrieve workflows from the database"""
        return Workflow.query.order_by(Workflow.created_at.desc()).paginate(
            page=page, 
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def get_workflow_by_id(workflow_id):
        """Retrieve a specific workflow by its ID"""
        return Workflow.query.get(workflow_id)

    @staticmethod
    def create_workflow(**data):
        if not data.get('name'):
            raise ValueError('Workflow name is required')
        
        # Add any other validation rules here
        
        workflow = Workflow(**data)
        db.session.add(workflow)
        db.session.commit()
        return workflow
    
    @staticmethod
    def delete_workflow(workflow_id):
        """Delete a workflow by its ID"""
        workflow = Workflow.query.get(workflow_id)
        if workflow:
            db.session.delete(workflow)
            db.session.commit()
        else:
            raise ValueError(f"Workflow with ID {workflow_id} not found")
