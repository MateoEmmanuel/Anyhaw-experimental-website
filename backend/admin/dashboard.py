from flask import Blueprint, render_template, session, redirect, url_for

admin_dashboard = Blueprint('admin_dashboard', __name__)

@admin_dashboard.route('/admin/dashboard')
def admin_index():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_auth.admin_login'))

    admin_name = session.get('admin_username')
    return render_template('admin_index.html', admin_name=admin_name)
