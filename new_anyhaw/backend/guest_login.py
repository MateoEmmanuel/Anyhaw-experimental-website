from flask import request, jsonify
from backend.dbconnection import create_connection

def guest_login():
    data = request.json
    guest_username = data.get("guest_username")
    contact_number = data.get("contact_number")

    if not guest_username or not contact_number:
        return jsonify({"message": "Missing guest username or contact number"}), 400

    conn = create_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    # Check if the guest already exists
    cursor.execute(
        "SELECT * FROM guest_accounts WHERE guest_username = %s AND contact_number = %s",
        (guest_username, contact_number)
    )
    existing_guest = cursor.fetchone()

    if existing_guest:
        conn.close()
        return jsonify({
            "message": "Guest login successful",
            "guest": {
                "guest_id": existing_guest["guest_id"],
                "guest_username": existing_guest["guest_username"],
                "contact_number": existing_guest["contact_number"]
            },
            "role": "guest"
        }), 200

    # Insert new guest
    cursor.execute(
        "INSERT INTO guest_accounts (guest_username, contact_number) VALUES (%s, %s)",
        (guest_username, contact_number)
    )
    conn.commit()

    guest_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "New guest account created",
        "guest": {
            "guest_id": guest_id,
            "guest_username": guest_username,
            "contact_number": contact_number
        },
        "role": "guest"
    }), 201
