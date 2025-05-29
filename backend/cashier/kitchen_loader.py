from flask import Blueprint, render_template, send_file, redirect, url_for, session, jsonify
from backend.dbconnection import create_connection
import pymysql
import io

cashier_bp = Blueprint('cashier_bp', __name__)

@cashier_bp.route('/cashier_loader')
def cashier_loader():
    return render_template('kitchen_lobby.html')

@cashier_bp.route('/profile_pic')
def profile_pic():
    user_id = session.get('user_id')
    user_role = session.get('role')

    if not user_id or not user_role:
        return redirect(url_for('static', filename='assets/images/default_profile.png'))

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Proper call to stored procedure
        cursor.callproc('GetProfileImageByRole', (user_id, user_role))

        for result in cursor.stored_results():
            data = result.fetchone()

        if data and data[0]:
            return send_file(io.BytesIO(data[0]), mimetype='image/jpeg')
        else:
            return redirect(url_for('static', filename='assets/images/default_profile.png'))

    except Exception as e:
        print(f"Error retrieving profile picture: {e}")
        return redirect(url_for('static', filename='assets/images/default_profile.png'))
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@cashier_bp.route('/get_username')
def get_username():
    user_id = session.get('user_id')
    role = session.get('role')

    if not user_id or not role:
        return jsonify({'error': 'Not logged in'}), 401

    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()

        cursor.callproc('GetUsernameByRole', (user_id, role))

        for result in cursor.stored_results():
            data = result.fetchone()

        if data and data[0]:
            return jsonify({'username': data[0]})
        return jsonify({'username': None})

    except Exception as e:
        print("Error fetching username:", e)
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
