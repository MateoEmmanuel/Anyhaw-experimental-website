from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.dbconnection import create_connection
from werkzeug.utils import secure_filename
cashier_settings_bp = Blueprint('cashier_settings', __name__)

import pymysql

# This route handles the update of cashier account information
@cashier_settings_bp.route('/backend/cashier/update_account', methods=['POST'])
def update_account():
    try:
        data = request.get_json()
        account_id = session.get('user_id')  # Ensure user is logged in

        if not account_id:
            return jsonify({"message": "Unauthorized"}), 401

        # Extract data from request
        firstname = data.get('firstname')
        middlename = data.get('middlename')
        lastname = data.get('lastname')
        email = data.get('email')
        contactnumber = data.get('contactnumber')

        # Connect to DB and call stored procedure
        conn = pymysql.connect(**create_connection())
        cursor = conn.cursor()
        cursor.callproc('UpdatePersonalAccount', (
            firstname,
            middlename,
            lastname,
            contactnumber,
            email,
            account_id
        ))
        conn.commit()

        return jsonify({"message": "Account updated successfully!"}), 200

    except Exception as e:
        print(f"Error updating account: {e}")
        return jsonify({"message": "An error occurred"}), 500

    finally:
        if conn:
            conn.close()