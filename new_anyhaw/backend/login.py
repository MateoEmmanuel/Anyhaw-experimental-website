from flask import request, jsonify, session
from backend.dbconnection import create_connection
import bcrypt

def login():
    data = request.json
    username_or_email = data.get("usernameOrEmail")
    password = data.get("password")

    conn = create_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    user = None
    role = None

    if "@" in username_or_email:
        cursor.execute("SELECT * FROM restaurant_accounts WHERE email = %s", (username_or_email,))
    else:
        cursor.execute("SELECT * FROM restaurant_accounts WHERE username = %s", (username_or_email,))
    
    result = cursor.fetchone()
    if result:
        user = result
        role = result["account_type"].capitalize()

    if not user:
        if "@" in username_or_email:
            cursor.execute("SELECT * FROM customer_accounts WHERE email = %s", (username_or_email,))
        else:
            cursor.execute("SELECT * FROM customer_accounts WHERE customer_username = %s", (username_or_email,))
        
        result = cursor.fetchone()
        if result:
            user = result
            role = "Customer"

    conn.close()

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        session["user_id"] = user.get("account_id") or user.get("customer_id")
        session["role"] = role

        # ADDITION: Store username in session for UI display
        session["username"] = user.get("username") or user.get("customer_username")

        return jsonify({
            "message": "Login successful",
            "user": {
                "email": user["email"],
                "role": role
            }
        }), 200
    else:
        return jsonify({"message": "Invalid email/username or password"}), 401
