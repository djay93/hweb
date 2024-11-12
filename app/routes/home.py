from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
def index():
    """
    Display the dashboard.
    """
    activity_logs = []
    return render_template('dashboard.html', activity_logs=activity_logs)


# Home route
@home_bp.route('/')
def home():
    return "App is up & running!"
    