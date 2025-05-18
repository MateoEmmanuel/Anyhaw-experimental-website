from flask import Blueprint, render_template
from backend.dbconnection import create_connection

cashier_payment_bp = Blueprint('cashier_payment', __name__, url_prefix='/cashier')

@cashier_payment_bp.route('/payment_module/<int:order_id>')
def payment_module(order_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the specific order by order_id and with Pending status
    cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s AND order_status = 'Pending'", (order_id,))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        return "Order not found or already processed", 404

    # Fetch the order items for this order_id
    cursor.execute("SELECT * FROM processing_order_items WHERE order_ID = %s", (order_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pass a single order (not a list) to the template
    return render_template('payment_module.html', order=order, items=items)
