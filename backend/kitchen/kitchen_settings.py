from flask import Blueprint, request, jsonify, session 
from backend.dbconnection import create_connection
import base64
import bcrypt

kitchen_settings_bp = Blueprint('kitchen_settings', __name__)

@kitchen_settings_bp.route('/update_account_info', methods=['POST'])
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


@kitchen_settings_bp.route('/get_user_account_info')
def get_user_account_info():
    conn = None
    cursor = None
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        conn = create_connection()
        cursor = conn.cursor()

        cursor.callproc('getaccountinfo_personel', (user_id,))
        result_data = None

        for result in cursor.stored_results():
            result_data = result.fetchone()
            break

        if result_data:
            return jsonify({
                'username': result_data[0],
                'first_name': result_data[1],
                'middle_name': result_data[2],
                'last_name': result_data[3],
                'contact_number': result_data[4],
                'email': result_data[5],
                'position_name': result_data[6]
            }), 200
        else:
            return jsonify({'error': 'User data not found'}), 404

    except Exception as e:
        print(f"[ERROR] get_user_account_info: {e}")
        return jsonify({'error': 'Server error while fetching account info'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@kitchen_settings_bp.route('/change_password', methods=['POST'])
def change_password():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid request data"}), 400

        account_id = session.get('user_id')
        if not account_id:
            return jsonify({"message": "Unauthorized"}), 401

        old_password = data.get('old_password', '').strip()
        new_password = data.get('new_password', '').strip()

        if not old_password or not new_password:
            return jsonify({"message": "Password fields cannot be empty"}), 400

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM restaurant_accounts WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "User not found"}), 404

        stored_hash = result[0]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')

        if not bcrypt.checkpw(old_password.encode('utf-8'), stored_hash):
            return jsonify({"message": "Old password is incorrect"}), 400

        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "UPDATE restaurant_accounts SET password = %s WHERE account_id = %s",
            (new_hashed_password.decode('utf-8'), account_id)
        )

        conn.commit()
        return jsonify({"message": "Password changed successfully!"}), 200

    except Exception as e:
        print(f"[ERROR] change_password: {e}")
        return jsonify({"message": "Server error occurred while changing password"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# updating profile picture
@kitchen_settings_bp.route('/update_profile_picture', methods=['POST'])
def update_profile_picture():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = session['user_id']
    file = request.files.get('profilePic')

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    image_blob = file.read()

    conn = None
    cursor = None

    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.callproc('UpdateProfilePicture_personel', (user_id, image_blob))
        conn.commit()

        return jsonify({'message': 'Profile picture updated successfully'}), 200

    except Exception as e:
        print(f"[ERROR] update_profile_picture: {e}")
        return jsonify({'error': 'Failed to update profile picture'}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close() 