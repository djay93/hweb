from flask import Blueprint, render_template

data_prep_bp = Blueprint('data_prep', __name__)

@data_prep_bp.route('/hmda')
def hmda_jobs():
    return render_template('data_prep/hmda/list_hmda_jobs.html')

@data_prep_bp.route('/data-prep-flows')
def data_prep_flows():
    return render_template('data_prep/data_prep_flows.html')