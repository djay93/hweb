from flask import Blueprint, request, render_template, redirect, url_for
from app.extensions import db
from app.services import WorkflowService

workflow_bp = Blueprint('workflows', __name__)

@workflow_bp.route('/', methods=['GET'])
def list_workflows():
    workflows = WorkflowService.get_all_workflows()
    return render_template('workflows/index.html', workflows=workflows)

@workflow_bp.route('/new', methods=['GET'])
def new_workflow():
    return render_template('workflows/new.html')

@workflow_bp.route('/', methods=['POST'])
def create_workflow():
    data = request.form
    
    name = data.get('name')
    description = data.get('description')

    if not name:
        return render_template('workflows/new.html', error='Workflow name is required')

    try:
        workflow = WorkflowService.create_workflow(name=name, description=description)
        return redirect(url_for('workflows.workflow_details', workflow_id=workflow.id))
    except Exception as e:
        return render_template('workflows/new.html', error=str(e))

@workflow_bp.route('/<int:workflow_id>', methods=['GET'])
def workflow_details(workflow_id):
    workflow = WorkflowService.get_workflow_by_id(workflow_id)
    if not workflow:
        return redirect(url_for('workflows.list_workflows', error='Workflow not found'))
    return render_template('workflows/show.html', workflow=workflow)
