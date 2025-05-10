from flask import request, jsonify
from backend.dbconnection import create_connection
import bcrypt

def login():
    data = request.json
    username_or_email = data.get("usernameOrEmail")  # Get the value for email or username
    password = data.get("password")

    conn = create_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    
    # First, try querying the restaurant_accounts table
    if "@" in username_or_email:  # If it's an email
        cursor.execute("SELECT * FROM restaurant_accounts WHERE email = %s", (username_or_email,))
    else:  # If it's a username
        cursor.execute("SELECT * FROM restaurant_accounts WHERE username = %s", (username_or_email,))
    
    user = cursor.fetchone()

    # If no user found in restaurant_accounts, check the customer_accounts table
    if not user:
        if "@" in username_or_email:  # If it's an email
            cursor.execute("SELECT * FROM customer_accounts WHERE email = %s", (username_or_email,))
        else:  # If it's a username
            cursor.execute("SELECT * FROM customer_accounts WHERE customer_username = %s", (username_or_email,))
        
        user = cursor.fetchone()

    conn.close()

    # Check if a user was found and if the password is correct
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        # Determine the role
        if "restaurant_accounts" in user:
            # This user is from restaurant_accounts, use account_type as role
            role = user["account_type"]
        else:
            # This user is from customer_accounts, role is "customer"
            role = "customer"
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "email": user["email"],
                "role": role
            }
        }), 200
    else:
        return jsonify({"message": "Invalid email/username or password"}), 401
