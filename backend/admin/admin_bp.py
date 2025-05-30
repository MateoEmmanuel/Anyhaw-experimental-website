import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# Configuration
UPLOAD_FOLDER = 'static/uploads/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Utility function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Dummy "logged in" user simulation (replace with real user session in production)
current_user = {
    "username": "admin",
    "profile_pic": "default.png"
}


@admin_bp.route('/')
def admin_dashboard():
    return render_template('admin/dashboard.html', user=current_user)


@admin_bp.route('/profile_pic')
def profile_pic():
    """Serve the current profile picture."""
    filename = current_user.get("profile_pic", "default.png")
    return send_from_directory(UPLOAD_FOLDER, filename)


@admin_bp.route('/update_profile_pic', methods=['POST'])
def update_profile_pic():
    if 'profile_pic' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['profile_pic']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)

        # Ensure upload directory exists
        os.makedirs(save_path, exist_ok=True)

        # Save file
        file.save(os.path.join(save_path, filename))

        # Update "user" data (in real world: update DB)
        current_user['profile_pic'] = filename

        return jsonify({"success": True, "filename": filename}), 200

    return jsonify({"error": "Invalid file type"}), 400

