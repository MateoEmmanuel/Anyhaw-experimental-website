from flask import Blueprint, render_template, request, jsonify, session
from backend.dbconnection import create_connection
from backend.cashier.reciepts.print_reciept import print_receipt_by_order_id
from decimal import Decimal, ROUND_UP

cashier_delivery_logging_bp = Blueprint('payment_delivery_payment_loader', __name__)

PRICE_PER_METER = Decimal('0.5')  # example price per meter for delivery fee, adjust as needed

@cashier_delivery_logging_bp.route('/payment_delivery_payment_module/<int:order_id>', methods=['GET', 'POST'])
def delivery_payment_payment_module(order_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        try:
            transaction_id = request.form.get("transactionID")
            order_id = request.form.get("orderId")
            
            # Get order info
            cursor.execute("SELECT * FROM ordered_logs WHERE Transaction_ID = %s", (transaction_id,))
            order = cursor.fetchone()
            if not order:
                cursor.close()
                conn.close()
                print(f"[DEBUG] Received transaction ID: {transaction_id}")  # Debugging line

                return jsonify(status='error', message='Order not found'), 404


            ordered_logs_id = order["Or_Logs_ID"]
            order_type = order["order_type"]

            if order_type == 'delivery':
                # Update order_status and delivery_payment_status if delivery
                cursor.execute("UPDATE ordered_logs SET status = 'paid' WHERE Or_Logs_ID = %s", (ordered_logs_id,))

                if order_id is not None:
                    cursor.execute("Delete processing_orders WHERE order_ID = %s", (order_id,))

                conn.commit()
                cursor.close()
                conn.close()
                return jsonify(status='success')

            else:
                cursor.close()
                conn.close()
                return jsonify(status='error', message=('message', 'Unknown error')), 500

        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify(status='error', message=str(e)), 500

    # GET request: load order, items, discounts for payment form (same for all)

    
    cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s AND order_status != 'pending'", (order_id,))
    customeridgetter = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        return "Order not found or already processed", 404

    customer_id = customeridgetter.get('customer_id')

    if customer_id:
        cursor.execute("SELECT * FROM customer_accounts WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if customer:
            customer['customer_name'] = " ".join(filter(None, [customer['Fname'], customer['Mname'], customer['Lname']]))
            customer['customer_contact'] = customeridgetter['contact_number']

        cursor.execute("SELECT * FROM customer_locations WHERE customer_id = %s", (customer_id,))
        location = cursor.fetchone()

        if location:
            full_address = f"{location['Street_Address']}, {location['Barangay_Subdivision']}, " \
                        f"{location['City_Municipality']}, {location['Province_Region']} " \
                        f"(Landmark: {location['landmark']})"
            customer['customer_location'] = full_address
        else:
            customer['customer_location'] = "No saved address"

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
    
    cursor.execute("""
        SELECT SUM(Total_Item_Price) as 'total_price' 
            FROM `processing_order_items` WHERE order_ID = %s
    """, (order_id,))
    result = cursor.fetchone()
    total_price = result['total_price'] if result['total_price'] else 0.0
    print(f"Total price for order {order_id}: {total_price}")
    
    cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s", (order_id,))
    order = cursor.fetchone()
    if not order:
                cursor.close()
                conn.close()
                return jsonify(status='error', message='Order not found'), 404

    order_type = order['order_type']
    delivery_distance = order.get('delivery_distance') or 0.0

    if order_type == 'delivery':
                # Delivery: no discount, delivery fee applied, payment status unpaid
                discount_id = None
                discount_percent = Decimal('0.0')
                delivery_fee = PRICE_PER_METER * Decimal(delivery_distance)
                total_price += delivery_fee
                

                # No cash validation for delivery (assumed unpaid or online)
                discounted_total = total_price.quantize(Decimal('0.01'), rounding=ROUND_UP)


    cursor.close()
    conn.close()

    return render_template('payment_delivery_payment.html', order=order, items=items, total_price=total_price, delivery_fee=delivery_fee)
