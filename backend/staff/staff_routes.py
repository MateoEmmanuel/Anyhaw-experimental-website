from flask import Blueprint, render_template, session, redirect, url_for, jsonify

staff_bp = Blueprint('staff_bp', __name__)

@staff_bp.route('/staff_loader')
def staff_loader():
    # Check if user is authenticated and has staff role
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':
        return render_template("staff/staff_index.html")
    else:
        # Redirect to login if not authenticated or not a staff
        return redirect(url_for("Index_home"))
        
@staff_bp.route('/get_staff_info')
def get_staff_info():
    # Example endpoint for fetching staff information
    if 'user_id' not in session or session['role'] != 'staff':
        return jsonify({"error": "Unauthorized"}), 403
        
    # Here you would typically fetch staff data from database
    # For now returning placeholder data
    return jsonify({
        "success": True,
        "staff_id": session.get('user_id'),
        "name": "Staff User"
    }) 