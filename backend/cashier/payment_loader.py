from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from backend.dbconnection import create_connection
from backend.cashier.reciepts.print_reciept import print_receipt_by_order_id
from decimal import Decimal, ROUND_UP

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
            discount_id = request.form.get("discountID")

            cursor.execute("SELECT Quantity, Price_Per_Item FROM processing_order_items WHERE order_ID = %s", (order_id,))
            items = cursor.fetchall()
            if not items:
                cursor.close()
                conn.close()
                return jsonify(status='error', message='No order items found'), 400

            total_price = sum(Decimal(item['Price_Per_Item']) * item['Quantity'] for item in items)
            
            if discount_id is None:
                discount_id = None
            elif discount_id == 0:
                discount_id = None
            elif discount_id == '0':
                discount_id = None
            else:
                discount_id = discount_id

            print(discount_id)

            if discount_id is not None:
                discounted_total = total_price - (total_price * discount_percent)
            else:
                discounted_total = total_price

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
            else:
                transaction_id = transaction_row['transaction_id']

            try:
                log_result = log_order_transaction(order_id, discount_id, payment_method, transaction_id)
                print(log_result)
                if log_result['status'] == 'success':
                    cursor.execute("UPDATE processing_orders SET order_status = 'preparing' WHERE order_ID = %s", (order_id,))
                    conn.commit()
                    return jsonify(status='success')
                else:
                    print(f"Warning: log_order_transaction returned error: {log_result.get('message')}")
                    return jsonify(f"Warning: log_order_transaction returned error: {log_result.get('message')}")
                    

            except Exception as e:
                print(f"Warning: log_order_transaction raised exception: {e}")
                return jsonify(f"Warning: log_order_transaction raised exception: {e}")


        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify(status='error', message=str(e)), 500


    # GET method part stays unchanged
    cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s AND order_status = 'pending'", (order_id,))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        return "Order not found or already processed", 404
    else:
        # get customer details
        customer_id = order.get('customer_id')

        if customer_id is not None:
            cursor.execute("SELECT * FROM customer_accounts WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()
            order['customer_name'] = " ".join(filter(None, [
                customer['Fname'],
                customer['Mname'],
                customer['Lname']
            ]))
            order['customer_contact'] = customer['contact_number']

            cursor.execute("SELECT * FROM customer_locations WHERE customer_id = %s", (customer_id,))
            location_recieve = cursor.fetchone()
            if location_recieve:
                order['customer_location'] = location_recieve['location']
            else:
                order['customer_location'] = "No saved address"
        else:
            order['customer_name'] = 'Walk-In Guest'
            order['customer_contact'] = ''
            order['customer_location'] = ''

            

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
        cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise Exception("Order not found.")

        order_type = order.get('order_type')
        customer_id = order.get('customer_id')
        order_list_id = order.get('order_list_id')
        cashier_id = session.get('user_id')

        cursor.execute("SELECT Quantity, Price_Per_Item FROM processing_order_items WHERE order_ID = %s", (order_id,))
        items = cursor.fetchall()
        total_price = sum(Decimal(item['Price_Per_Item']) * item['Quantity'] for item in items)

        # Handle discount ID properly
        print('discount ID: ', discount_id)
        
        
        if discount_id is not None and discount_id != 0:
            cursor.execute("SELECT Discount_Percent FROM discount_table WHERE Discount_ID = %s", (discount_id,))
            discount_row = cursor.fetchone()

            if discount_row and 'Discount_Percent' in discount_row:
                discount_percent = Decimal(discount_row['Discount_Percent'])
                print('discount Percent: ', discount_percent)
            else:
                raise Exception("Discount not found in discount_table.")
        else:
            discount_id = None  # Ensure it's NULL in the DB
            discount_percent = Decimal('0.0')
            print('discount Percent: ', discount_percent)

        discount_price = (total_price * discount_percent).quantize(Decimal('0.01'), rounding=ROUND_UP)
        discounted_total = (total_price - discount_price).quantize(Decimal('0.01'), rounding=ROUND_UP)

        payment_method_clean = payment_method.replace("-option", "")

        if order_type == 'delivery':
            status = "unpaid"
        elif order_type in ['dine-in', 'take-out']:
            status = "paid"
        else:
            raise Exception("Unknown order type")

        print('id:', order_id)
        print('transaction id:', transaction_id)
        print('cashier id:', cashier_id)
        print('total price:', total_price)
        print('discount id:', discount_id)
        print('discount percent:', discount_percent)
        print('discounted total:', discounted_total)
        print('payment method:', payment_method_clean)
        print('order type:', order_type)
        print('customer id:', customer_id)
        print('status:', status)

        cursor.execute("SET @p_or_logs_id = 0")

        cursor.execute("CALL loging_walk_in_order(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @p_or_logs_id)", (
            order_id,
            transaction_id,
            cashier_id,
            total_price,
            discount_id,
            discounted_total,
            payment_method_clean,
            order_type,
            customer_id,
            status,
        ))

        cursor.execute("SELECT @p_or_logs_id AS or_logs_id")
        result = cursor.fetchone()
        or_logs_id = result['or_logs_id'] if result else None

        if not or_logs_id:
            raise Exception("Failed to get Ordered_Logs ID.")

        print("Logging order items with:")
        print("Order List ID:", order_list_id)
        print("Ordered Logs ID:", or_logs_id)

        try:
            cursor.callproc('log_order_items', (order_list_id, or_logs_id))
            conn.commit()
            return {'status': 'success'}
        except Exception as e:
            print("Error in logging order items:", str(e))
            raise

    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

    finally:
        cursor.close()
        conn.close()

