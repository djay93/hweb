from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from app.services.hmda_service import HMDAService 
from app.forms import HmdaJobDetailsForm
from app.models.enum import WorkflowType, JobStatus

hmda_bp = Blueprint('hmda', __name__)
hmda_api_bp = Blueprint('hmda_api', __name__)

@hmda_bp.route('/', methods=['GET'])
def list_hmda_jobs():
    """
    Display a paginated list of HMDA jobs.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 5
    search = request.args.get('search', '').strip().lower()
    pagination = HMDAService.get_hmda_jobs(page, per_page, search)
    return render_template('hmda/list_hmda_jobs.html', hmda_reports=pagination.items, pagination=pagination)

@hmda_bp.route('/new', methods=['GET'])
def new_hmda_job():
    """
    Display the form for creating a new HMDA job.
    """
    form = HmdaJobDetailsForm()
    return render_template('hmda/new_hmda_job.html', form=form)


@hmda_bp.route('/<int:hmda_id>/details', methods=['GET'])
def view_hmda_job(hmda_id):
    """
    Display the details of an existing HMDA job.
    """
    hmda_job = HMDAService.get_hmda_job_by_id(hmda_id)
    if not hmda_job:
        flash('HMDA Job not found', 'error')
        return redirect(url_for('hmda.list_hmda_jobs'))
    
    # Set the form data
    form = HmdaJobDetailsForm(obj=hmda_job)
    form.workflow_type.data = hmda_job.workflow_type.name
    form.workflow_id.data = hmda_job.workflow_id

    # Set other fields
    hmda_job_data = hmda_job.to_dict()

    # render the template
    return render_template('hmda/view_hmda_job.html', form=form, hmda_job=hmda_job_data)
    

@hmda_bp.route('/<int:hmda_id>/edit', methods=['GET'])
def edit_hmda_job(hmda_id):
    """
    Display the form for editing an existing HMDA job.
    """
    hmda_job = HMDAService.get_hmda_job_by_id(hmda_id)
    if not hmda_job:
        flash('HMDA Job not found', 'error')
        return redirect(url_for('hmda.list_hmda_jobs'))
    
    # Set the form data
    form = HmdaJobDetailsForm(obj=hmda_job)
    form.workflow_type.data = hmda_job.workflow_type.name
    form.workflow_id.data = hmda_job.workflow_id

    # Set other fields
    hmda_job_data = hmda_job.to_dict()

    # render the template
    return render_template('hmda/edit_hmda_job.html', form=form, hmda_job=hmda_job_data)

############# API Routes #############
@hmda_api_bp.route('/<int:job_id>', methods=['DELETE'])
def api_delete_hmda_job(job_id):
    """
    Deletes an existing HMDA job.
    """
    try:
        HMDAService.delete_hmda_job(job_id)
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@hmda_api_bp.route('/', methods=['POST'])
def api_create_hmda_job():
    """
    Saves a new HMDA job.
    """
    data = request.get_json() 

    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    # Extract and validate data
    try:
        name = data.get('name')
        workflow_id = data.get('workflow_id')
        workflow_type = data.get('workflow_type', WorkflowType.HMDA.name)
        status = data.get('status', JobStatus.PENDING.name)
        
        start_time = None
        end_time = None
        next_run_time = None
        if data.get('start_time'):
            start_time = datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M')
        if data.get('end_time'):
            end_time = datetime.strptime(data.get('end_time'), '%Y-%m-%d %H:%M')
        if data.get('next_run_time'):
            next_run_time = datetime.strptime(data.get('next_run_time'), '%Y-%m-%d')
        
        workflow_tasks = data.get('workflow_tasks', [])
        #job_status = JobStatus[status].name if status else JobStatus.PENDING.name

        # Create a new HMDA process using form data
        hmda_process = HMDAService.create_hmda_job(
            name=name,
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            start_time=start_time,
            end_time=end_time,
            status=status,
            next_run_time=next_run_time
        )

        # Create the job steps
        HMDAService.create_hmda_job_steps(hmda_process.id, workflow_tasks)

        return jsonify({
            'message': 'HMDA process created successfully!',
            'hmda_process_id': hmda_process.id
        }), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Error creating HMDA process: {str(e)}'}), 500