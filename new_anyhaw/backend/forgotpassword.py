from flask import request, jsonify, session
from backend.dbconnection import create_connection
import random, string, smtplib, os, bcrypt
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()  # Load EMAIL_ADDRESS and EMAIL_PASSWORD from .env

# Function to send email with the verification code
def send_email(to_email, code):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    subject = "Anyhaw Letchon Manok Restaurant: Account Password Reset"
    body = f"""\
Dear Valued Customer,

We have received a request to reset the password for your Anyhaw Letchon Manok Restaurant account associated with your email address. Your password reset verification code is:

{code}

This code is valid for 30 minutes. Please enter this code in the application to proceed with resetting your password.

If you did not initiate this request, please disregard this message. Someone may have entered your email address by mistake.

This email address is linked to your Anyhaw Letchon Manok Restaurant account. If this association is incorrect, please contact our support team immediately.

Thank you for choosing Anyhaw Letchon Manok Restaurant.

Best regards,

The Anyhaw Letchon Manok Restaurant Team
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def forgot_password():
    data = request.json
    email = data.get("email")
    
    conn = create_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    # Search both restaurant_accounts and customer_accounts for the email
    cursor.execute("""
        SELECT email FROM restaurant_accounts WHERE email = %s
        UNION 
        SELECT email FROM customer_accounts WHERE email = %s
    """, (email, email))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({"message": "Email not found"}), 404

    # Generate a verification code
    code = ''.join(random.choices(string.digits, k=6))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)

    # Store the reset code in the session (for a short time)
    session['reset_code'] = {'email': email, 'code': code, 'expires_at': expires_at}

    conn.close()

    # Send email with the verification code
    send_email(email, code)

    return jsonify({"message": "Verification code sent to your email."}), 200

def verify_reset_code():
    data = request.json
    email = data.get("email")
    code = data.get("code")

    # Retrieve code from session
    session_data = session.get('reset_code')

    if not session_data:
        return jsonify({"message": "No reset request found. Please request a reset first."}), 400

    # Check if the email and code match, and that the code is not expired
    if session_data['email'] != email or session_data['code'] != code:
        return jsonify({"message": "Invalid code"}), 400

    if datetime.now(timezone.utc) > session_data['expires_at']:
        return jsonify({"message": "Code expired"}), 400

    # If valid, clear the session data
    session.pop('reset_code', None)
    return jsonify({"message": "Code verified. You can now reset your password."}), 200

def reset_password():
    data = request.json
    email = session.get("email")
    new_password = data.get("new_password")

    # Validate new_password
    if not new_password:
        return jsonify({"message": "New password is required"}), 400

    # Hash the new password
    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = create_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()

    # Try updating password in both tables
    cursor.execute("""
        UPDATE restaurant_accounts SET password = %s WHERE email = %s
    """, (hashed, email))
    if cursor.rowcount == 0:
        cursor.execute("""
            UPDATE customer_accounts SET password = %s WHERE email = %s
        """, (hashed, email))

    conn.commit()
    conn.close()

    # Clear the reset code from the session after successful password update
    session.pop('reset_code', None)

    return jsonify({"message": "Password updated successfully"}), 200
