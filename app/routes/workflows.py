from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash
from marshmallow import ValidationError
from app.services import WorkflowService
from app.models.enum import WorkflowType
from app.schemas import WorkflowSchema, WorkflowTaskSchema

workflow_bp = Blueprint('workflows', __name__)
workflow_api_bp = Blueprint('workflow_api', __name__)

# Initialize Marshmallow schemas
workflow_schema = WorkflowSchema()
task_schema = WorkflowTaskSchema(many=True)

# ----------------------------------------
# Web UI Routes (Form-based, returns HTML)
# ----------------------------------------

@workflow_bp.route('/', methods=['GET'])
def list_workflows():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = WorkflowService.get_workflows(page, per_page)
    return render_template('workflows/workflow_list.html', workflows=pagination.items, pagination=pagination)


@workflow_bp.route('/new', methods=['GET', 'POST'])
def new_workflow():
    form = WorkflowForm()
    if form.validate_on_submit():
        try:
            workflow = WorkflowService.create_workflow(
                    name=form.name.data,
                    description=form.description.data,
                    workflow_type=form.workflow_type.data
                )
            flash('Workflow created successfully!', 'success')
            return redirect(url_for('workflows.list_workflows'))
        except Exception as e:
            flash(f'Error creating workflow: {str(e)}', 'danger')
            return render_template('workflows/workflow_new.html', workflow=form, error=str(e))
    
    return render_template('workflows/workflow_new.html', workflow=form)

@workflow_bp.route('/<int:workflow_id>', methods=['GET', 'POST'])
def edit_workflow(workflow_id):
    workflow = WorkflowService.get_workflow_by_id(workflow_id)
    if not workflow:
        flash('Workflow not found', 'error')
        return redirect(url_for('workflows.list_workflows'))

    form = WorkflowForm(obj=workflow)
    form.workflow_type.choices = [(type.name, type.value) for type in WorkflowType]
    
    if request.method == 'GET':
        # Set the dropdown value
        form.workflow_type.data = workflow.workflow_type.name
        return render_template('workflows/workflow_edit.html', form=form, workflow=workflow)
    
    if form.validate_on_submit():
        try:
            # Update the workflow
            WorkflowService.update_workflow(
                workflow_id=workflow_id,
                name=form.name.data,
                description=form.description.data,
                workflow_type=form.workflow_type.data
            )
            flash('Workflow updated successfully!', 'success')
            return redirect(url_for('workflows.edit_workflow', workflow_id=workflow_id))
        except Exception as e:
            flash(f'Error updating workflow: {str(e)}', 'danger')
    
    return render_template('workflows/workflow_edit.html', form=form, workflow=workflow)


# ----------------------------------------
# REST API Routes (JSON responses)
# ----------------------------------------
@workflow_api_bp.route('/', methods=['POST'])
def api_create_workflow():
    data = request.get_json()

    # Validate and deserialize input data
    try:
        workflow_data = workflow_schema.load(data)
        workflow = WorkflowService.create_workflow(**workflow_data)
        return jsonify(workflow_schema.dump(workflow)), 201
    except ValidationError as ve:
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@workflow_api_bp.route('/<int:workflow_id>', methods=['GET'])
def api_get_workflow(workflow_id):
    workflow = WorkflowService.get_workflow_by_id(workflow_id)
    if not workflow:
        return jsonify({'error': 'Workflow not found'}), 404

    return jsonify(workflow_schema.dump(workflow))

@workflow_api_bp.route('/<int:workflow_id>', methods=['DELETE'])
def api_delete_workflow(workflow_id):
    try:
        WorkflowService.delete_workflow(workflow_id)
        return jsonify({'message': 'Workflow deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@workflow_api_bp.route('/<int:workflow_id>/tasks', methods=['GET'])
def api_get_workflow_tasks(workflow_id):
    try:
        tasks = WorkflowService.get_workflow_tasks(workflow_id)
        return jsonify({
            'message': 'No tasks found' if not tasks else 'Tasks retrieved successfully',
            'tasks': task_schema.dump(tasks)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
