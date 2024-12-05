from flask import Blueprint, render_template

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/policy-configuration')
def policy_configuration():
    return render_template('settings/policy_configuration.html')

@settings_bp.route('/permissions-roles')
def permissions_roles():
    return render_template('settings/permissions_roles.html')

@settings_bp.route('/application-settings')
def application_settings():
    return render_template('settings/application_settings.html')
