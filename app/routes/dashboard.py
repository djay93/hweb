from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    activity_logs = []
    return render_template('dashboard/overview.html', activity_logs=activity_logs)

@dashboard_bp.route('/dashboard/overview')
def overview():
    activity_logs = []
    return render_template('dashboard/overview.html', activity_logs=activity_logs)

@dashboard_bp.route('/dashboard/recent-activities')
def activities():
    return render_template('dashboard/recent_activities.html')

@dashboard_bp.route('/dashboard/data-prep-status')
def data_prep_status():
    return render_template('dashboard/data_prep_status.html')

# Home route
@dashboard_bp.route('/status')
def home():
    return "App is up & running!"
    