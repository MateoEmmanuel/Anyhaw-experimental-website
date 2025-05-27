from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from backend.dbconnection import create_connection
from backend.cashier.reciepts.print_reciept import print_receipt_by_order_id
from decimal import Decimal, ROUND_UP, ROUND_HALF_UP

cashier_payment_delivery_bp = Blueprint('cashier_payment_delivery', __name__, url_prefix='/cashier')

@cashier_payment_delivery_bp.route('/payment_delivery_module/<int:order_id>', methods=['GET', 'POST'])
def payment_delivery_module(order_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    price_per_meter = Decimal('0.5')

    if request.method == 'POST':
        try:
            print(
                "post request received for order ID:", order_id)
            
            
            cursor.execute("SELECT customer_id FROM processing_orders WHERE order_ID = %s", (order_id,))
            customer_naming = cursor.fetchone()

            customer_id = customer_naming.get('customer_id')
            
            cashier_id = session.get('user_id')
            
            
            cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s", (order_id,))
            order = cursor.fetchone()
            transaction_id = order.get('transaction_id')
            payment_method = order.get('delivery_payment_method')
            
            cursor.execute("SELECT delivery_distance FROM processing_orders WHERE order_ID = %s", (order_id,))
            delivery_distance_row = cursor.fetchone()
            cursor.execute("SELECT Quantity, Price_Per_Item FROM processing_order_items WHERE order_ID = %s", (order_id,))
            items = cursor.fetchall()
            if not items:
                cursor.close()
                conn.close()
                return jsonify(status='error', message='No order items found'), 400
            
            print("Delivery distance:", delivery_distance_row['delivery_distance'])
            print("Price per meter:", Decimal(price_per_meter))
            print("overall price:", sum(Decimal(item['Price_Per_Item']) * item['Quantity'] for item in items))
            original_price = sum(Decimal(item['Price_Per_Item']) * item['Quantity'] for item in items)

            # Delivery: no discount, delivery fee applied, payment status unpaid
            delivery_fee = Decimal(price_per_meter) * Decimal(delivery_distance_row['delivery_distance'])
            total_price = original_price + delivery_fee


           # Ensure all numeric values are converted to Decimal



            # Insert into Ordered_Logs
            cursor.execute("""
                INSERT INTO Ordered_Logs 
                (Transaction_ID, customer_id, cashier_id, Original_Price, Discount_ID, Total_Price, payment_method, order_type, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'delivery', 'unpaid')
            """, (transaction_id, customer_id, cashier_id, original_price, None, total_price, payment_method))
            
            ordered_log_id = cursor.lastrowid

            # Fetch all items from processing_order_items for this order
            cursor.execute("""
                SELECT item_id, Item_Type, Quantity, Price_Per_Item, Total_Item_Price
                FROM processing_order_items
                WHERE order_ID = %s
            """, (order_id,))
            items = cursor.fetchall()

            # Insert each item into Ordered_Items referencing the new Or_Logs_ID
            for item in items:
                cursor.execute("""
                    INSERT INTO Ordered_Items (Or_Logs_ID, item_id, Item_Type, Quantity, Price_Per_Item)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    ordered_log_id,
                    item['item_id'],
                    item['Item_Type'],
                    item['Quantity'],
                    item['Price_Per_Item'],
                ))

            conn.commit()

            cursor.execute("Update processing_orders SET order_status = 'preparing' WHERE order_ID = %s", (order_id,))
            conn.commit()
            cursor.close()
            conn.close()


            return jsonify(status='success', message='Order moved to Ordered_Logs as unpaid delivery')
        


        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify(status='error', message=str(e)), 500
        


# ------------------------------------------------------------------------------------------------------------------------------------------

    # GET: fetch order info from processing_orders
    cursor.execute("SELECT * FROM processing_orders WHERE order_ID = %s", (order_id,))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        return "Order not found in processing orders", 404

    customer_id = order.get('customer_id')
    if customer_id:
        cursor.execute("SELECT * FROM customer_accounts WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        order['customer_name'] = " ".join(filter(None, [customer['Fname'], customer['Mname'], customer['Lname']]))
        order['customer_contact'] = customer['contact_number']

        cursor.execute("SELECT * FROM customer_locations WHERE customer_id = %s", (customer_id,))
        location = cursor.fetchone()

        if location:
            full_address = f"{location['Street_Address']}, {location['Barangay_Subdivision']}, " \
                        f"{location['City_Municipality']}, {location['Province_Region']} " \
                        f"(Landmark: {location['landmark']})"
            order['customer_location'] = full_address
        else:
            order['customer_location'] = "No saved address"


    print(f"Processing order ID: {order_id} for customer ID: {customer_id}")

    # Calculate delivery fee here and add it to the order dict
    delivery_fee = round(order.get('delivery_distance', Decimal('0.00')) * Decimal('0.05'), 2) if order.get('delivery_distance') is not None else Decimal('0.00')

    order['delivery_fee'] = delivery_fee

    # Fetch order items with item names
    cursor.execute("SELECT * FROM processing_order_items WHERE order_ID = %s", (order_id,))
    raw_items = cursor.fetchall()

    items = []
    for item in raw_items:
        item_name = "Unknown Item"
        item_type = item['Item_Type']
        item_id = item['item_id']

        # Lookup item name based on type and id
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

    # Calculate total price from processing_order_items
    cursor.execute("""
        SELECT SUM(Total_Item_Price) AS total_price
        FROM processing_order_items
        WHERE order_ID = %s
    """, (order_id,))
    total_row = cursor.fetchone()
    total_price = total_row['total_price'] if total_row and total_row['total_price'] else 0.0

    # Fetch discounts (optional for the template)
    cursor.execute("SELECT Discount_ID, Discount_Name, Discount_Percent FROM Discount_Table")
    discounts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'payment_delivery_module.html',
        customer_id=customer_id,
        order=order,
        items=items,
        total_price=total_price,
        discounts=discounts,
        price_per_meter=price_per_meter,
    )
