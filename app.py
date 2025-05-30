import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv("C:/xampp/htdocs/new_anyhaw_kim/new_anyhaw/static/assets/localfile/restaurantsetting.env")
print("EMAIL_ADDRESS:", os.getenv("EMAIL_ADDRESS"))
print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))

from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from flask_cors import CORS
from functools import wraps
from datetime import datetime

# Import the organized menu data
from organized_menu import best_sellers, others, drinks, combo_meals, desserts, sizzling_meal, silog, additional_menu_items

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
from backend.admin.admin_loader import admin_bp
from backend.admin.admin_settings import admin_settings_bp
from backend.staff.staff_routes import staff_bp
from backend.delivery.delivery_routes import delivery_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)

# In-memory storage for orders
orders_storage = []

# Function to get menu categories directly from app.py
def get_categories():
    # Use the imported menu data from organized_menu.py
    categories = [
        {
            "title": "Best Sellers",
            "icon": url_for('static', filename='assets/images/categoriesIcon/maincourse.png'),
            "menus": best_sellers
        },
        {
            "title": "Others",
            "icon": url_for('static', filename='assets/images/categoriesIcon/maincourse.png'),
            "menus": others
        },
        {
            "title": "Drinks",
            "icon": url_for('static', filename='assets/images/categoriesIcon/milktea.png'),
            "menus": drinks
        },
        {
            "title": "Combo Meals",
            "icon": url_for('static', filename='assets/images/categoriesIcon/maincourse.png'),
            "menus": combo_meals
        },
        {
            "title": "Desserts",
            "icon": url_for('static', filename='assets/images/categoriesIcon/frappe.png'),
            "menus": desserts
        },
        {
            "title": "Sizzling Meal",
            "icon": url_for('static', filename='assets/images/categoriesIcon/maincourse.png'),
            "menus": sizzling_meal
        },
        {
            "title": "Silog",
            "icon": url_for('static', filename='assets/images/categoriesIcon/maincourse.png'),
            "menus": silog
        }
    ]
    
    # Create "All menu" category by collecting all menus from other categories
    all_menus = []
    for category in categories:
        all_menus.extend(category["menus"])
    
    # Remove duplicates by menu_title and sort alphabetically
    unique_menus = {menu["menu_title"]: menu for menu in all_menus}
    all_menus = sorted(unique_menus.values(), key=lambda x: x["menu_title"])

    # Insert "All menu" category at the beginning
    categories.insert(0, {
        "title": "All menu",
        "icon": url_for('static', filename='assets/images/categoriesIcon/allmenu.png'),
        "menus": all_menus
    })
    
    return categories

# API route for placing orders
@app.route('/api/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['orderType', 'paymentMethod', 'cartItems', 'total', 'created_at']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Validate cartItems is a list
    if not isinstance(data.get('cartItems'), list):
        return jsonify({'error': 'cartItems must be a list'}), 400

    # Generate a new order ID
    new_id = f"#{(max(int(o['id'].lstrip('#')) for o in orders_storage) + 1) if orders_storage else 51240}"
    
    # Create the new order
    new_order = {
        "id": new_id,
        "customer_table": "Table N/A" if data['orderType'].lower() == 'to-go' else f"Table {len(orders_storage) + 1}",
        "status": "waiting",
        "order_type": data['orderType'].capitalize(),
        "items": [
            {
                "ordername": item.get('title', 'Unknown'),
                "quantity": int(item.get('quantity', 0)),
                "price": float(item.get('price', 0.0)),
                "image": item.get('picture', '')
            } for item in data['cartItems']
        ],
        "total": float(data.get('total', 0.0)),
        "created_at": datetime.fromisoformat(data['created_at']).isoformat(),
        "total_items": sum(int(item.get('quantity', 0)) for item in data['cartItems'])
    }

    # Add customer info if provided
    if 'customerInfo' in data:
        new_order['customer_info'] = data['customerInfo']

    # Add the new order to storage
    orders_storage.append(new_order)
    print(f"New order added: {new_order}")  # Debug output
    return jsonify({'message': 'Order placed successfully!', 'order_id': new_id}), 200

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

app.register_blueprint(admin_bp, url_prefix="/backend/admin")
app.register_blueprint(admin_settings_bp, url_prefix="/backend/admin", methods=["POST"])

# Register new blueprints for staff and delivery
app.register_blueprint(staff_bp, url_prefix="/backend/staff")
app.register_blueprint(delivery_bp, url_prefix="/backend/delivery")

# Security middleware
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('Index_home'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                return jsonify({"error": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/")
def Index_home():
    # Check if a user is already logged in by checking session
    if 'user_id' in session and 'role' in session:
        role = session['role']
        # Redirect to role-specific UI
        if role == "admin":
            return redirect(url_for("admin_bp.admin_loader")) # admin main UI lobby
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
        return redirect(url_for("admin_bp.admin_loader"))
    else:
        # Redirect to login if not authenticated or not an admin
        return redirect(url_for("Index_home"))

@app.route("/staff_ui")
@login_required
@role_required(['staff'])
def staff_ui():
    return render_template("staff_ui.html")

@app.route("/delivery_ui")
@login_required
@role_required(['delivery'])
def delivery_ui():
    return render_template("delivery_ui.html")

@app.route("/customer_ui")
@login_required
@role_required(['customer'])
def customer_ui():
    categories = get_categories()
    return render_template("menu.html", categories=categories)

@app.route("/menu")
def menu():
    categories = get_categories()
    return render_template("menu.html", categories=categories)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True) 