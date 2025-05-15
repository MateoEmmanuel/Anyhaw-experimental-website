from flask import Blueprint, request, jsonify, session
from backend.dbconnection import create_connection
import pymysql
import bcrypt

cashier_settings_bp = Blueprint('cashier_settings', __name__)

@cashier_settings_bp.route('/update_account', methods=['POST'])
def update_account():
    conn = None
    try:
        data = request.get_json()
        account_id = session.get('user_id')

        if not account_id:
            return jsonify({"message": "Unauthorized"}), 401

        firstname = data.get('firstname')
        middlename = data.get('middlename')
        lastname = data.get('lastname')
        email = data.get('email')
        contactnumber = data.get('contactnumber')

        conn = create_connection() 
        cursor = conn.cursor()

        cursor.callproc('updateaccountinfo_personel', (
            account_id,
            firstname,
            middlename,
            lastname,
            contactnumber,
            email
        ))

        conn.commit()
        return jsonify({"message": "Account updated successfully!"}), 200

    except Exception as e:
        print(f"Error updating account: {e}")
        return jsonify({"message": "An error occurred"}), 500

    finally:
        if conn:
            conn.close()

@cashier_settings_bp.route('/get_user_account_info')
def get_user_account_info():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Call the updated IN-only procedure
        cursor.callproc('getaccountinfo_personel', (user_id,))

        # Retrieve the result set
        for result in cursor.stored_results():
            data = result.fetchone()

        if data:
            return jsonify({
                'first_name': data[0],
                'middle_name': data[1],
                'last_name': data[2],
                'contact_number': data[3],
                'email': data[4],
                'position_name': data[5]
            })
        else:
            return jsonify({'error': 'No data found'}), 404

    except Exception as e:
        print("Error fetching account info:", e)
        return jsonify({'error': 'Server error'}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@cashier_settings_bp.route('/change_password', methods=['POST'])
def change_password():
    conn = None
    try:
        data = request.get_json()
        account_id = session.get('user_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not account_id:
            return jsonify({"message": "Unauthorized"}), 401

        if not old_password or not new_password:
            return jsonify({"message": "Password fields cannot be empty"}), 400

        conn = create_connection()
        cursor = conn.cursor()

        # Fetch hashed password (stored as bytes or string)
        cursor.execute("SELECT password FROM restaurant_accounts WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "User not found"}), 404

        stored_hash = result[0]

        # bcrypt stores hashes as bytes, so encode strings if needed
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')

        if not bcrypt.checkpw(old_password.encode('utf-8'), stored_hash):
            return jsonify({"message": "Old password is incorrect"}), 400

        # Hash the new password with bcrypt
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # Store new hashed password (decode to string if your DB expects string)
        cursor.execute("UPDATE restaurant_accounts SET password = %s WHERE account_id = %s",
                       (new_hashed_password.decode('utf-8'), account_id))
        conn.commit()

        return jsonify({"message": "Password changed successfully!"}), 200

    except Exception as e:
        print(f"Error changing password: {e}")
        return jsonify({"message": "An error occurred"}), 500

    finally:
        if conn:
            conn.close()