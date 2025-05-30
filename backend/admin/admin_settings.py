from flask import Blueprint, request, jsonify, session 
from backend.dbconnection import create_connection
import base64
import bcrypt

admin_settings_bp = Blueprint('admin_settings_bp', __name__)

@admin_settings_bp.route('/update_account_info', methods=['POST'])
def update_account_info():
    conn = None
    try:
        data = request.get_json()
        account_id = session.get('user_id')

        if not account_id:
            return jsonify({"message": "Unauthorized"}), 401

        user_name = data.get('username')
        firstname = data.get('firstname')
        middlename = data.get('middlename')
        lastname = data.get('lastname')
        email = data.get('email')
        contactnumber = data.get('contactnumber')

        conn = create_connection() 
        cursor = conn.cursor()

        cursor.callproc('updateaccountinfo_personel', (
            account_id,
            user_name,
            firstname,
            middlename,
            lastname,
            email,
            contactnumber
        ))

        conn.commit()
        return jsonify({"message": "Account updated successfully!"}), 200

    except Exception as e:
        print(f"Error updating account: {e}")
        return jsonify({"message": "An error occurred"}), 500

    finally:
        if conn:
            conn.close()

@admin_settings_bp.route('/get_user_account_info')
def get_user_account_info():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.callproc('get_account_info_by_id', (user_id,))

        for result in cursor.stored_results():
            account_info = result.fetchone()

        if account_info:
            return jsonify(account_info), 200
        else:
            return jsonify({"error": "Account not found"}), 404

    except Exception as e:
        print(f"Error retrieving account info: {e}")
        return jsonify({"error": "Error retrieving account information"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@admin_settings_bp.route('/update_profile_picture', methods=['POST'])
def update_profile_picture():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    if 'profile_pic' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['profile_pic']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the image file
        image_data = file.read()
        
        conn = create_connection()
        cursor = conn.cursor()
        
        # Call stored procedure to update profile picture
        cursor.callproc('update_profile_picture', (user_id, image_data))
        conn.commit()
        
        return jsonify({"message": "Profile picture updated successfully"}), 200
    
    except Exception as e:
        print(f"Error updating profile picture: {e}")
        return jsonify({"error": "Failed to update profile picture"}), 500
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@admin_settings_bp.route('/change_password', methods=['POST'])
def change_password():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({"error": "Old and new passwords are required"}), 400
    
    # Password validation
    if len(new_password) < 8 or len(new_password) > 12:
        return jsonify({"error": "Password must be 8-12 characters long"}), 400
    
    if not any(c.isupper() for c in new_password):
        return jsonify({"error": "Password must contain at least one uppercase letter"}), 400
    
    if not any(c.islower() for c in new_password):
        return jsonify({"error": "Password must contain at least one lowercase letter"}), 400
    
    if not any(c.isdigit() for c in new_password):
        return jsonify({"error": "Password must contain at least one number"}), 400
    
    if not any(not c.isalnum() for c in new_password):
        return jsonify({"error": "Password must contain at least one special character"}), 400
    
    conn = None
    cursor = None
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get current password
        cursor.execute("SELECT password FROM restaurant_accounts WHERE account_id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Verify old password
        if not bcrypt.checkpw(old_password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"error": "Incorrect old password"}), 400
        
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Update password
        cursor.execute(
            "UPDATE restaurant_accounts SET password = %s WHERE account_id = %s",
            (hashed_password.decode('utf-8'), user_id)
        )
        conn.commit()
        
        return jsonify({"message": "Password updated successfully"}), 200
    
    except Exception as e:
        print(f"Error changing password: {e}")
        return jsonify({"error": "An error occurred while changing password"}), 500
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close() 