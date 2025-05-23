from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from backend.dbconnection import create_connection
from backend.cashier.reciepts.print_reciept import print_receipt_by_order_id
from decimal import Decimal

cashier_payment_bp = Blueprint('cashier_payment', __name__, url_prefix='/cashier')

@cashier_payment_bp.route('/payment_module/<int:order_id>', methods=['GET', 'POST'])
def payment_module(order_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        try:
            payment_method = request.form['paymentMethod']
            cash_given = request.form.get('cashGiven', type=float)
            discount_percent = request.form.get('discountPercent', type=float) or 0.0
            discount_percent = Decimal(discount_percent)
            
            cursor.execute("SELECT Quantity, Price_Per_Item FROM processing_order_items WHERE order_ID = %s", (order_id,))
            items = cursor.fetchall()
            if not items:
                cursor.close()
                conn.close()
                return jsonify(status='error', message='No order items found'), 400

            total_price = sum(Decimal(item['Price_Per_Item']) * item['Quantity'] for item in items)
            discounted_total = total_price * (Decimal('1') - discount_percent / Decimal('100'))

            if payment_method == "gcash":
                return jsonify(status='error', message='GCash payment not implemented yet'), 400

            elif payment_method == 'cash-option' and (cash_given is None or Decimal(cash_given) < discounted_total):
                cursor.close()
                conn.close()
                return jsonify(status='error', message='Insufficient cash provided'), 400

            cursor.execute("SELECT transaction_id FROM processing_orders WHERE order_ID = %s", (order_id,))
            transaction_row = cursor.fetchone()
            if not transaction_row or not transaction_row['transaction_id']:
                cursor.close()
                conn.close()
                return jsonify(status='error', message='Missing transaction ID'), 400
            transaction_id = transaction_row['transaction_id']

            try:
                log_result = log_order_transaction(order_id, discount_percent, payment_method, transaction_id)
                if log_result['status'] != 'success':
                    print(f"Warning: log_order_transaction returned error: {log_result.get('message')}")
            except Exception as e:
                print(f"Warning: log_order_transaction raised exception: {e}")

            cursor.execute("UPDATE processing_orders SET order_status = 'preparing' WHERE order_ID = %s", (order_id,))
            conn.commit()

            cursor.close()
            conn.close()
            return jsonify(status='success', transaction_id=transaction_id)

        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify(status='error', message=str(e)), 500


    # GET method part stays unchanged
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
        item_name = "ERROR-RETRIEVING ITEM NAME"
        item_type = item.get('Item_Type')
        item_id = item.get('item_id')

        if item_type == 'normal':
            cursor.execute("SELECT Food_Name FROM food_list WHERE Food_ID = %s", (item_id,))
            result = cursor.fetchone()
            if result:
                item_name = result['Food_Name']

        elif item_type == 'dessert':
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

    # Get available discounts
    cursor.execute("SELECT Discount_ID, Discount_Name, Discount_Percent FROM Discount_Table")
    discounts = cursor.fetchall()

    cursor.execute("""
        SELECT SUM(Total_Item_Price) AS total_price
        FROM processing_order_items
        WHERE order_ID = %s
    """, (order_id,))
    result = cursor.fetchone()
    total_price = result['total_price'] if result['total_price'] else 0.0

    cursor.close()
    conn.close()

    return render_template('payment_module.html', order=order, items=items, total_price=total_price, discounts=discounts)


def log_order_transaction(order_id, discount_id, payment_method, transaction_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get order details and order_list_id
        cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise Exception("Order not found.")

        customer_id = order.get('customer_id')
        guest_id = order.get('guest_id')
        order_list_id = order.get('order_list_id')

        if customer_id:
            customer_id_to_use = customer_id
            account_type = 'customer'
        else:
            customer_id_to_use = None
            account_type = 'guest'

        cashier_id = session.get('user_id')

        print("Discount ID: ", discount_id)
        print("Discount percent: ", discount_percent)
        print("Discount Total", discounted_total)

        # Convert discount_id to int or None
        discount_id = int(discount_id) if discount_id and discount_id != '0' else None

        # Re-calculate total after discount (fetching percent by ID)
        cursor.execute("SELECT Quantity, Price_Per_Item FROM processing_order_items WHERE order_ID = %s", (order_id,))
        items = cursor.fetchall()
        total_price = sum(Decimal(item['Price_Per_Item']) * item['Quantity'] for item in items)

        # If there's a discount, fetch its percent
        if discount_id:
            cursor.execute("SELECT Discount_Percent FROM Discount_Table WHERE Discount_ID = %s", (discount_id,))
            percent_row = cursor.fetchone()
            if percent_row:
                discount_percent = Decimal(percent_row['Discount_Percent']) / Decimal('100')
            else:
                raise Exception("Invalid discount ID.")
        else:
            discount_percent = Decimal('0')

        discounted_total = total_price * (Decimal('1') - discount_percent)

        payment_method_clean = payment_method.replace("-option", "")
        order_type = 'walk-in'

        args = (
            order_id,
            transaction_id,
            cashier_id,
            discount_id,
            round(discounted_total, 2),
            payment_method_clean,
            order_type,
            customer_id_to_use,
            account_type,
            0  # OUT param
        )

        result_args = cursor.callproc('loging_walk_in_order', args)
        or_logs_id = result_args[9]
        if not or_logs_id:
            raise Exception("Failed to get Ordered_Logs ID.")

        cursor.callproc('log_order_items', (order_list_id, or_logs_id))
        conn.commit()
        return {'status': 'success'}

    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

    finally:
        cursor.close()
        conn.close()
