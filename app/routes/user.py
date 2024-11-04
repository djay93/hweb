from flask import Blueprint, render_template
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
def profile():
    return render_template('user/profile.html')

@user_bp.route('/settings', methods=['GET'])
def settings():
    return render_template('user/settings.html')

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('user/dashboard.html', now=datetime.now())


@user_bp.route('/logout', methods=['GET'])
def logout():
    return "TODO: Implement logout"