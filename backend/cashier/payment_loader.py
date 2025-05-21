from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from backend.dbconnection import create_connection
from backend.cashier.reciepts.print_reciept import print_receipt_by_order_id

cashier_payment_bp = Blueprint('cashier_payment', __name__, url_prefix='/cashier')

@cashier_payment_bp.route('/payment_module/<int:order_id>', methods=['GET', 'POST'])
def payment_module(order_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        payment_method = request.form['paymentMethod']
        cash_given = request.form.get('cashGiven', type=float)
        discount_percent = request.form.get('discountPercent', type=float) or 0.0

                # Re-fetch total
        cursor.execute("SELECT Quantity, Price_Per_Item FROM processing_order_items WHERE order_ID = %s", (order_id,))
        items = cursor.fetchall()
        total_price = sum(item['Price_Per_Item'] * item['Quantity'] for item in items)

                # Apply discount
        discounted_total = total_price * (1 - discount_percent / 100)

        if payment_method == 'cash-option' and cash_given < discounted_total:
                    cursor.close()
                    conn.close()
                    return "Insufficient cash provided", 400

        # Update order status
        cursor.execute("UPDATE processing_orders SET order_status = 'Preparing' WHERE order_ID = %s", (order_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('cashier_payment.payment_success', order_id=order_id))

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    # GET method
    cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s AND order_status = 'Pending'", (order_id,))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        return "Order not found or already processed", 404
    else:
        # get customer details
        customer_id = order.get('customer_id')
        guest_id = order.get('guest_id')

        if customer_id is not None:
            cursor.execute("SELECT * FROM customer_accounts WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()
            order['customer_name'] = customer['customer_name']
            order['customer_location'] = customer['customer_location']
            order['customer_contact'] = customer['contact_number']

        elif guest_id is not None:
            order['customer_name'] = order['guest_name']
            order['customer_location'] = order['guest_location']
            cursor.execute("SELECT contact_number FROM guest_accounts WHERE guest_id = %s", (guest_id,))
            result = cursor.fetchone()
            order['customer_contact'] = result['contact_number'] if result else "Unknown"

        else:
            cursor.close()
            conn.close()
            return "No customer or guest ID found for order.", 400

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

        # Get available discounts
    cursor.execute("SELECT Discount_ID, Discount_Name, Discount_Percent FROM Discount_Table")
    discounts = cursor.fetchall()

    cursor.close()
    conn.close()


    return render_template('payment_module.html', order=order, items=items, total_price=total_price, discounts=discounts)


@cashier_payment_bp.route('/update_order_status', methods=['POST'])
def update_order_status_route():
    data = request.get_json()
    order_id = data.get('order_id')
    payment_method = data.get('payment_method')  # 'cash' or 'online'
    discount_id = data.get('discount_id')  # Optional
    gcash_ref = data.get('gcash_ref') if payment_method == 'online' else None

    if not order_id or not payment_method:
        return jsonify(success=False, message="Missing required data"), 400

    cashier_id = session.get('cashier_id')
    if not cashier_id:
        return jsonify(success=False, message="Cashier not logged in"), 403

    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        # Get order
        cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            return jsonify(success=False, message="Order not found"), 404

        order_type = order['order_type']  # dine-in / take-out / delivery

        # Get order items
        cursor.execute("SELECT * FROM processing_order_items WHERE order_ID = %s", (order_id,))
        items = cursor.fetchall()
        if not items:
            return jsonify(success=False, message="No order items found"), 404

        # Always update the status
        cursor.execute("UPDATE processing_orders SET order_status = 'preparing' WHERE order_ID = %s", (order_id,))
        cursor.execute("UPDATE processing_order_items SET Prep_status = 'preparing' WHERE order_ID = %s", (order_id,))

        # Only insert and print for dine-in / take-out
        if order_type in ['dine-in', 'take-out']:
            total_price = sum(item['Total_Item_Price'] for item in items)

            # Apply discount if provided
            if discount_id:
                cursor.execute("SELECT Discount_Value FROM Discount_Table WHERE Discount_ID = %s", (discount_id,))
                discount_row = cursor.fetchone()
                if discount_row:
                    discount_value = float(discount_row['Discount_Value'])
                    total_price *= (1 - discount_value / 100)

            # Insert into Ordered_Logs
            cursor.execute("""
                INSERT INTO Ordered_Logs (
                    Transaction_ID, customer_id, customer_account_type, cashier_id, Discount_ID,
                    Total_Price, payment_method, gcash_ref, order_type, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'paid')
            """, (
                str(order['transaction_id']),
                order['customer_id'],
                'guest' if order['guest_id'] else 'customer',
                cashier_id,
                discount_id,
                round(total_price, 2),
                payment_method,
                gcash_ref,
                'walk-in'
            ))

            or_logs_id = cursor.lastrowid

            # Insert items
            for item in items:
                cursor.execute("""
                    INSERT INTO Ordered_Items (
                        Or_Logs_ID, item_id, Item_Type, Quantity, Price_Per_Item
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    or_logs_id,
                    item['item_id'],
                    item['Item_Type'],
                    item['Quantity'],
                    item['Price_Per_Item']
                ))

            conn.commit()
            cursor.close()
            conn.close()

            # ✅ Print receipt
            print_receipt_by_order_id(or_logs_id)

        else:
            # Just commit the status update for delivery
            conn.commit()
            cursor.close()
            conn.close()

        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

