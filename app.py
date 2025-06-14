import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv("C:/xampp/htdocs/new_anyhaw_kim/new_anyhaw/static/assets/localfile/restaurantsetting.env")
print("EMAIL_ADDRESS:", os.getenv("EMAIL_ADDRESS"))
print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))

from flask import Flask, redirect, render_template, session, url_for
from flask_cors import CORS

from backend.login import login
from backend.register import register_bp
from backend.dbconnection import create_connection
from backend.forgotpassword import forgot_password
from backend.forgotpassword import send_email
from backend.forgotpassword import verify_reset_code
from backend.forgotpassword import reset_password
from backend.cashier.cashier_settings import cashier_settings_bp
from backend.cashier.cashier_loader import cashier_bp
from backend.logout import logout_bp
from backend.cashier.cashier_system import cashier_system_bp
from backend.cashier.cashier_orderque_loader import cashier_orderqueue_bp
from backend.cashier.payment_loader import cashier_payment_bp
from backend.cashier.reciepts.print_reciept import print_receipt_by_order_id
from backend.cashier.order_status_loader import cashier_orderstatus_bp
from backend.cashier.cashier_served_table_loader import cashier_served_order_bp
from backend.cashier.cashier_delivery_status_loader import cashier_delivery_status_loader_bp
from backend.cashier.cashier_dinein_history import cashier_dinein_history_bp
from backend.cashier.cashier_takeout_history import cashier_takeout_history_bp
from backend.cashier.cashier_delivery_history import cashier_delivery_history_bp
from backend.cashier.payment_loader_delivery import cashier_payment_delivery_bp
from backend.cashier.payment_delivery_payment_loader import cashier_delivery_logging_bp
from backend.kitchen.kitchen_loader import kitchen_bp
from backend.kitchen.kitchen_orderque_loader import kitchen_orderqueue_bp
from backend.kitchen.kitchen_orderque_loader_public import kitchen_public_order_queue_loader_bp
from backend.kitchen.kitchen_settings import kitchen_settings_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)

# Register blueprints
app.register_blueprint(register_bp, url_prefix="/backend")
app.add_url_rule('/login', view_func=login, methods=["POST"])
app.add_url_rule('/forgot-password', view_func=forgot_password, methods=["POST"])
app.add_url_rule('/verify-recovery-code', view_func=verify_reset_code, methods=["POST"])
app.add_url_rule('/reset-password', view_func=reset_password, methods=["POST"])
app.add_url_rule('/send-email', view_func=send_email, methods=["POST"])
app.register_blueprint(cashier_settings_bp, url_prefix="/backend/cashier", methods=["POST"])
app.register_blueprint(logout_bp)
app.register_blueprint(cashier_bp, url_prefix='/backend/cashier')
app.register_blueprint(cashier_system_bp, url_prefix='/backend/cashier_system')
app.register_blueprint(cashier_orderqueue_bp, url_prefix='/backend/cashier')
app.register_blueprint(cashier_payment_bp, url_prefix='/backend/cashier')
app.register_blueprint(cashier_orderstatus_bp, url_prefix='/backend/cashier')
app.register_blueprint(cashier_served_order_bp, url_prefix='/backend/cashier')
app.register_blueprint(cashier_delivery_status_loader_bp, url_prefix="/backend/cashier")
app.register_blueprint(cashier_dinein_history_bp, url_prefix="/backend/cashier")
app.register_blueprint(cashier_takeout_history_bp, url_prefix="/backend/cashier")
app.register_blueprint(cashier_delivery_history_bp, url_prefix="/backend/cashier")
app.register_blueprint(cashier_payment_delivery_bp, url_prefix="/backend/cashier")
app.register_blueprint(cashier_delivery_logging_bp, url_prefix="/backend/cashier")

app.register_blueprint(kitchen_bp, url_prefix="/backend/kitchen")
app.register_blueprint(kitchen_orderqueue_bp, url_prefix="/backend/kitchen")
app.register_blueprint(kitchen_public_order_queue_loader_bp, url_prefix="/backend/kitchen")
app.register_blueprint(kitchen_settings_bp, url_prefix="/backend/kitchen", methods=["POST"])

@app.route("/")
def Index_home():
    # Check if a user is already logged in by checking session
    if 'user_id' in session and 'role' in session:
        role = session['role']
        # Redirect to role-specific UI
        if role == "admin":
            return redirect(url_for("admin_ui")) # admin main UI lobby
        elif role == "customer": 
            return redirect(url_for("customer_ui")) # customer main UI lobby
        elif role == "staff":
            return redirect(url_for("staff_ui")) # staff main UI lobby
        elif role == "Cashier":
            return redirect(url_for("cashier_bp.cashier_loader"))  # cashier main UI lobby
        elif role == "kitchen":
            return redirect(url_for("kitchen_bp.kitchen_loader")) # kitchen main UI lobby
        elif role == "delivery":
            return redirect(url_for("delivery_ui")) # delivery main UI lobby
        else:
            # Unknown role, just return to index
            return render_template("index.html")
    else:
        # No user session — show the main landing page
        return render_template("index.html")  # This will render index.html from the templates folder

@app.route("/admin_ui")
def admin_ui():
    # Check if user is authenticated and has admin role
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
        return render_template("admin_ui.html")
    else:
        # Redirect to login if not authenticated or not an admin
        return redirect(url_for("Index_home"))

@app.route("/customer_ui")
def customer_ui():
    return render_template("customer_ui.html")

if __name__ == "__main__":
    app.run(debug=True)
    