from flask import Blueprint, request, jsonify
from backend.dbconnection import create_connection
import bcrypt

register_bp = Blueprint("register_bp", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check if email and password are provided
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    # Create database connection
    conn = create_connection()
    if not conn:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    try:
        cursor = conn.cursor(dictionary=True)

        # Check if the email already exists in the database
        cursor.execute("SELECT * FROM customer_accounts WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email already registered."
            }), 409

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert new user into the database
        cursor.execute(
            "INSERT INTO customer_accounts (customer_username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw.decode("utf-8"))
        )
        conn.commit()

        # Return success message
        return jsonify({
            "success": True,
            "message": "Registered successfully."
        }), 201

    except Exception as e:
        # Log the exception for better debugging
        print(f"Error: {str(e)}")  # Print error to the console
        return jsonify({
            "success": False,
            "message": f"Registration failed: {str(e)}"
        }), 500

    finally:
        conn.close()
        