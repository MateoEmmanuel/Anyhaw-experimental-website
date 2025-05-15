from flask import Blueprint, render_template, send_file, redirect, url_for, session
from backend.dbconnection import create_connection
import pymysql
import io

cashier_bp = Blueprint('cashier_bp', __name__)

@cashier_bp.route('/cashier_loader')  # ✅ Remove the leading /cashier
def cashier_loader():
    return render_template('cashier_lobby.html')

@cashier_bp.route('/cashier/profile_pic')
def profile_pic():
    conn = None
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    # If user is not logged in, serve default profile picture
    if not user_id or not user_role:
        return redirect(url_for('static', filename='assets/images/default_profile.png'))

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Call stored procedure to retrieve image blob
        cursor.callproc('GetProfileImageByRole', (user_id, user_role))

        result = cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving profile picture: {e}")
        return redirect(url_for('static', filename='assets/images/default_profile.png'))
    finally:
        if conn:
            conn.close()

    # If image blob exists, return it
    if result and result[0]:
        return send_file(io.BytesIO(result[0]), mimetype='image/jpeg')
    else:
        return redirect(url_for('static', filename='assets/images/default_profile.png'))

@cashier_bp.route('/cashier/get_username')
def get_username(user_id, role):
    conn = None
    user_id = session.get('user_id')
    role = session.get('user_role')
    try:
        conn = create_connection()
        if not conn:
            print("Database connection failed")
            return None
        cursor = conn.cursor()

        cursor.callproc('GetUsernameByRole', (user_id, role))
        result = cursor.fetchone()

        if result:
            return result[0]  # the username
        return None
    except Exception as e:
        print("Error fetching username:", e)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()