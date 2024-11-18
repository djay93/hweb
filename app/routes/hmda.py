import logging
import json
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from marshmallow import ValidationError
from app.services import HMDAService
from app.models.enum import JobStatus, WorkflowType, TriggerType
from app.schemas import JobSchema, JobTaskSchema, JobSchemaWithoutTasks

hmda_bp = Blueprint('hmda', __name__)
hmda_api_bp = Blueprint('hmda_api', __name__)

# Initialize Marshmallow schemas
hmda_job_schema = JobSchema()
hmda_job_tasks_schema = JobTaskSchema(many=True)
hmda_jobs_without_tasks_schema = JobSchemaWithoutTasks(many=True)

# Set up logging
logger = logging.getLogger(__name__)

# ----------------------------------------
# Web UI Routes
# ----------------------------------------

@hmda_bp.route('/', methods=['GET'])
def list_hmda_jobs():
    # Initial data for the page
    initial_data = {
        'page': request.args.get('page', 1, type=int),
        'per_page': request.args.get('per_page', 10, type=int),
        'search': request.args.get('search', ''),
        'hmda_jobs': [],  # Will be populated by API call
        'pagination': {}  # Will be populated by API call
    }
    
    return render_template('hmda/list_hmda_jobs.html', initial_data=json.dumps(initial_data))

@hmda_bp.route('/new', methods=['GET'])
def new_hmda_job():
    form_data = {
        "name": "",
        "workflow_type": WorkflowType.HMDA.name,
        "workflow_id": None,
        "status": JobStatus.NEW.name,
        "next_run_time": None,
        "start_time": None,
        "end_time": None,
        "workflow_type_options": WorkflowType.choices(),
        "status_options": JobStatus.choices(),
        "workflow_options": [{"id": w.id, "name": w.name} for w in HMDAService.get_hmda_workflows()]
    }
    serialized_data = json.dumps(form_data)
    logger.info("Loaded form for creating a new HMDA job.")
    return render_template('hmda/new_hmda_job.html', form_data=serialized_data)


@hmda_bp.route('/<int:hmda_id>/details', methods=['GET'])
def view_hmda_job(hmda_id):
    try:
        # get job details
        hmda_job = HMDAService.get_hmda_job_by_id(hmda_id)
        if not hmda_job:
            logger.warning(f"HMDA Job with ID {hmda_id} not found.")
            flash('HMDA Job not found', 'error')
            return redirect(url_for('hmda.list_hmda_jobs')), 404

        # serialize job data
        hmda_job_data = hmda_job_schema.dump(hmda_job)

        # get form options
        form_options = {
            "workflow_type_options": WorkflowType.choices(),
            "status_options": JobStatus.choices(),
            "task_type_options": TriggerType.choices(),
            "workflow_options": [{"id": w.id, "name": w.name} for w in HMDAService.get_hmda_workflows()]
        }

        logger.info(f"Loaded edit form for HMDA Job ID {hmda_id}.")
    except Exception as e:
        logger.error(f"Error loading HMDA Job ID {hmda_id} for editing: {str(e)}")
        flash("An error occurred while loading the job for editing.", "error")
        return redirect(url_for('hmda.list_hmda_jobs')), 500

    return render_template('hmda/view_hmda_job.html', form_data=json.dumps(hmda_job_data), form_options=json.dumps(form_options))


@hmda_bp.route('/<int:hmda_id>/edit', methods=['GET'])
def edit_hmda_job(hmda_id):
    try:
        # get job details
        hmda_job = HMDAService.get_hmda_job_by_id(hmda_id)
        if not hmda_job:
            logger.warning(f"HMDA Job with ID {hmda_id} not found.")
            flash('HMDA Job not found', 'error')
            return redirect(url_for('hmda.list_hmda_jobs')), 404

        # serialize job data
        hmda_job_data = hmda_job_schema.dump(hmda_job)

        # get form options
        form_options = {
            "workflow_type_options": WorkflowType.choices(),
            "status_options": JobStatus.choices(),
            "task_type_options": TriggerType.choices(),
            "workflow_options": [{"id": w.id, "name": w.name} for w in HMDAService.get_hmda_workflows()]
        }

        logger.info(f"Loaded edit form for HMDA Job ID {hmda_id}.")
    except Exception as e:
        logger.error(f"Error loading HMDA Job ID {hmda_id} for editing: {str(e)}")
        flash("An error occurred while loading the job for editing.", "error")
        return redirect(url_for('hmda.list_hmda_jobs')), 500

    return render_template('hmda/edit_hmda_job.html', form_data=json.dumps(hmda_job_data), form_options=json.dumps(form_options))


# ----------------------------------------
# API Routes
# ----------------------------------------

@hmda_api_bp.route('/', methods=['GET'])
def api_search_hmda_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', '').strip().lower()

    try:
        pagination = HMDAService.get_hmda_jobs(page, per_page, search)
        serialized_jobs = hmda_jobs_without_tasks_schema.dump(pagination.items)

        # Create pagination info dictionary
        pagination_info = {
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'next_num': pagination.next_num,
            'prev_num': pagination.prev_num
        }

        return jsonify({
            'hmda_jobs': serialized_jobs,
            'pagination': pagination_info
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving HMDA jobs: {str(e)}")
        return jsonify({'error': f'Error retrieving HMDA jobs: {str(e)}'}), 500


@hmda_api_bp.route('/<int:job_id>', methods=['DELETE'])
def api_delete_hmda_job(job_id):
    try:
        HMDAService.delete_hmda_job(job_id)
        logger.info(f"HMDA Job ID {job_id} deleted successfully.")
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Failed to delete HMDA Job ID {job_id}: {str(e)}")
        return jsonify({'error': f'Failed to delete job: {str(e)}'}), 400


@hmda_api_bp.route('/', methods=['POST'])
def api_create_hmda_job():
    body = request.get_json()
    if not body:
        logger.warning("Received invalid JSON payload.")
        return jsonify({'error': 'Invalid JSON payload'}), 400

    try:
        # Deserialize and validate job data
        job_data = hmda_job_schema.load(body.get("job_data"))
        logger.info("Validated HMDA job data successfully.")

        # Create the primary job
        hmda_job = HMDAService.create_hmda_job(job_data)
        logger.info(f"HMDA Job created successfully with ID {hmda_job.id}.")

        # Deserialize, validate, and create job tasks
        job_tasks_data = body.get('job_tasks_data', [])
        for task in job_tasks_data:
            task['job_id'] = hmda_job.id
        hmda_job_tasks_data = hmda_job_tasks_schema.load(job_tasks_data)
        HMDAService.create_hmda_job_tasks(hmda_job.id, hmda_job_tasks_data)
        logger.info(f"Job tasks for HMDA Job ID {hmda_job.id} created successfully.")

        # Respond with success
        return jsonify({
            'message': 'HMDA process created successfully!',
            'hmda_job_id': hmda_job.id
        }), 201

    except ValidationError as ve:
        logger.warning(f"Validation error creating HMDA job: {ve.messages}")
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        logger.error(f"Error creating HMDA process: {str(e)}")
        return jsonify({'error': f'Error creating HMDA process: {str(e)}'}), 500


@hmda_api_bp.route('/<int:job_id>', methods=['PUT'])
def api_update_hmda_job(job_id):
    body = request.get_json()
    if not body:
        logger.warning("Received invalid JSON payload.")
        return jsonify({'error': 'Invalid JSON payload'}), 400

    try:
        # Deserialize and validate job data
        job_data = hmda_job_schema.load(body)
        logger.info("Validated HMDA job data successfully.")

         # Extract tasks before updating job
        tasks = job_data.pop('tasks', [])

        # Update the primary job
        hmda_job = HMDAService.update_hmda_job(job_id, job_data)
        if not hmda_job:
            logger.warning(f"HMDA Job with ID {job_id} not found.")
            return jsonify({'error': 'Job not found'}), 404
        logger.info(f"HMDA Job {job_id} updated successfully.")

        # Update job tasks
        if tasks:
            logger.info(f"tasks: {tasks}")
            hmda_job_tasks_data = hmda_job_tasks_schema.load(tasks)
            HMDAService.update_hmda_job_tasks(job_id, hmda_job_tasks_data)
            logger.info(f"Job tasks for HMDA Job ID {job_id} updated successfully.")

        # Respond with success
        return jsonify({
            'message': 'HMDA process updated successfully!',
            'hmda_job_id': job_id
        }), 200

    except ValidationError as ve:
        logger.warning(f"Validation error updating HMDA job: {ve.messages}")
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        logger.error(f"Error updating HMDA process: {str(e)}")
        return jsonify({'error': f'Error updating HMDA process: {str(e)}'}), 500

@hmda_api_bp.route('/job-tasks/<int:job_task_id>/execute', methods=['POST'])
def api_execute_hmda_job_task(job_task_id):
    try:
        HMDAService.execute_hmda_job_task(job_task_id)
        return jsonify({'message': 'HMDA job task executed successfully!'}), 200
    except Exception as e:
        logger.error(f"Error executing HMDA job task: {str(e)}")
        return jsonify({'error': f'Error executing HMDA job task: {str(e)}'}), 500
