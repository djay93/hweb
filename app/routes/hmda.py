from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from app.services.hmda_service import HMDAService 
from app.services.workflow_service import WorkflowService
from app.forms.hmda import HmdaProcessForm
from app.models.enum import WorkflowType

hmda_bp = Blueprint('hmda', __name__)
hmda_api_bp = Blueprint('hmda_api', __name__)

@hmda_bp.route('/', methods=['GET'])
def list_hmda_weekly_reports():   
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = HMDAService.get_hmda_jobs(page, per_page)
    return render_template('hmda/hmda_weekly_list.html', hmda_reports=pagination.items, pagination=pagination)

@hmda_bp.route('/new', methods=['GET', 'POST'])
def new_hmda_weekly_report():
    form = HmdaProcessForm()

    workflows = WorkflowService.get_workflows() or []
    form.workflow_id.choices = [(workflow.id, workflow.name) for workflow in HMDAService.get_hmda_weekly_workflows()]
    form.workflow_type.data = WorkflowType.HMDA_WEEKLY.name

    if form.validate_on_submit():
        try:
            #Create a new HMDA process using form data
            hmda_process = HMDAService.create_hmda_job(
                name=form.name.data,
                workflow_id=form.workflow_id.data,
                workflow_type=form.workflow_type.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                status=form.status.data,
                next_run_time=form.next_run_time.data
            )
            flash('HMDA process created successfully!', 'success')
            return redirect(url_for('hmda.list_hmda_weekly_reports'))
        except Exception as e:
            flash(f'Error creating HMDA process: {str(e)}', 'danger')
            return render_template('hmda/hmda_weekly_new.html', form=form, error=str(e))

    return render_template('hmda/hmda_weekly_new.html', form=form)


# @hmda_api.route('/<int:id>', methods=['GET'])
# def get_hmda_weekly_report(id):
#     hmda_report = HMDAService.get_hmda_job(id)
#     return jsonify(hmda_report)

@hmda_api_bp.route('/<int:job_id>', methods=['DELETE'])
def api_delete_hmda_job(job_id):
    try:
        HMDAService.delete_hmda_job(job_id)
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400