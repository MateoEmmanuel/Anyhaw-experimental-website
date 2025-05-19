from flask import Blueprint, render_template, request, redirect, url_for
from backend.dbconnection import create_connection

cashier_payment_bp = Blueprint('cashier_payment', __name__, url_prefix='/cashier')

@cashier_payment_bp.route('/payment_module/<int:order_id>', methods=['GET', 'POST'])
def payment_module(order_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        payment_method = request.form['paymentMethod']
        cash_given = request.form.get('cashGiven', type=float)

        # Re-fetch total
        cursor.execute("SELECT Quantity, Price_Per_Item FROM processing_order_items WHERE order_ID = %s", (order_id,))
        items = cursor.fetchall()
        total_price = sum(item['Price_Per_Item'] * item['Quantity'] for item in items)

        if payment_method == 'cash-option' and cash_given < total_price:
            cursor.close()
            conn.close()
            return "Insufficient cash provided", 400

        # Update order status
        cursor.execute("UPDATE processing_orders SET order_status = 'Preparing' WHERE order_ID = %s", (order_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('cashier_payment.payment_success', order_id=order_id))

    # GET method
    cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s AND order_status = 'Pending'", (order_id,))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        return "Order not found or already processed", 404

    cursor.execute("SELECT * FROM processing_order_items WHERE order_ID = %s", (order_id,))
    raw_items = cursor.fetchall()

    items = []

    for item in raw_items:
        item_name = "ERROR-RETRIEVEING ITEM NAME"
        item_type = item.get('Item_Type')
        item_id = item.get('item_id')

        if item_type in ('normal'):
            cursor.execute("SELECT Food_Name FROM food_list WHERE Food_ID = %s", (item_id,))
            result = cursor.fetchone()
            if result:
                item_name = result['Food_Name']

        elif item_type in ('dessert'):
            cursor.execute("SELECT Dessert_Name FROM Dessert_list WHERE Dessert_ID = %s", (item_id,))
            result = cursor.fetchone()
            if result:
                item_name = result['Dessert_Name']

        elif item_type == 'drink':
            cursor.execute("SELECT Drink_Name FROM drink_list WHERE Drink_ID = %s", (item_id,))
            result = cursor.fetchone()
            if result:
                item_name = result['Drink_Name']

        elif item_type == 'combo':
            cursor.execute("SELECT Code_Name FROM Combo_Food_List WHERE Combo_List_ID = %s", (item_id,))
            result = cursor.fetchone()
            if result:
                item_name = result['Code_Name']

        item['Item_Name'] = item_name
        items.append(item)

    total_price = sum(item['Price_Per_Item'] * item['Quantity'] for item in items)

    cursor.close()
    conn.close()

    return render_template('payment_module.html', order=order, items=items, total_price=total_price)

@cashier_payment_bp.route('/update_order_status', methods=['POST'])
def update_order_status_route():
    from flask import jsonify
    data = request.get_json()
    order_id = data.get('order_id')
    new_status = data.get('new_status')

    if not order_id or not new_status:
        return jsonify(success=False, message="Missing order_id or new_status"), 400

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE processing_orders SET order_status = %s WHERE order_ID = %s", (new_status, order_id))
        cursor.execute("UPDATE processing_order_items SET Prep_status = 'preparing' WHERE order_ID = %s", (order_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500
