from flask import Blueprint, render_template, request, jsonify
from backend.dbconnection import create_connection

kitchen_orderqueue_bp = Blueprint('kitchen_orderqueue', __name__)

@kitchen_orderqueue_bp.route('/kitchen_public_order_queue_loader')
def kitchen_public_order_queue_loader():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get both 'preparing' and 'ready to serve' orders
        cursor.execute("""
            SELECT order_ID, transaction_id, table_number, order_status, order_type,
                DATE_FORMAT(order_time, '%M %d %Y / %h:%i:%s %p') AS order_time, customer_id
            FROM processing_orders 
            WHERE order_status IN ('preparing', 'serve', 'waiting for pickup')
            ORDER BY order_time DESC,
                    CASE order_type
                        WHEN 'dine-in' THEN 1
                        WHEN 'take-out' THEN 2
                        WHEN 'delivery' THEN 3
                        ELSE 4
                    END
        """)
        orders_data = cursor.fetchall()

        preparing_orders = []
        serving_orders = []

        for order in orders_data:
            order_id = order['order_ID']

            # Fetch items
            cursor.execute("""
                SELECT item_id, Item_Type, Quantity, Price_Per_Item, Total_Item_Price 
                FROM processing_order_items 
                WHERE order_ID = %s
            """, (order_id,))
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
                    cursor.execute("SELECT Dessert_Name FROM dessert_list WHERE Dessert_ID = %s", (item_id,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result['Dessert_Name']

                elif item_type == 'drink':
                    cursor.execute("SELECT Drink_Name FROM drink_list WHERE Drink_ID = %s", (item_id,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result['Drink_Name']

                elif item_type == 'combo':
                    cursor.execute("SELECT Code_Name FROM combo_food_list WHERE Combo_List_ID = %s", (item_id,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result['Code_Name']

                item['Item_Name'] = item_name
                items.append(item)

            # Customer info
            customer_id = order['customer_id']
            if customer_id:
                cursor.execute("""
                    SELECT CONCAT(ca.Lname, ', ', ca.Fname, ' ', ca.Mname) AS Customer_Name, 
                           ca.contact_number,
                           CONCAT(
                               cl.Street_Address, ', ',
                               cl.Barangay_Subdivision, ', ',
                               cl.City_Municipality, ', ',
                               cl.Province_Region, ' (Landmark: ',
                               cl.landmark, ')'
                           ) AS location
                    FROM customer_accounts ca
                    LEFT JOIN customer_locations cl ON ca.customer_id = cl.customer_id
                    WHERE ca.customer_id = %s
                """, (customer_id,))
                result = cursor.fetchone()
                customer_name = result['Customer_Name'] if result else "Unknown"
                customer_contact = result['contact_number'] if result else "Unknown"
                customer_location = result['location'] if result else "Unknown"
            else:
                customer_name = "Walk-In Guest"
                customer_contact = " "
                customer_location = " "

            order_data = {
                'order_ID': order['order_ID'],
                'transaction_id': order['transaction_id'],
                'table_number': order['table_number'],
                'order_status': order['order_status'],
                'order_type': order['order_type'],
                'order_time': order['order_time'],
                'customer': customer_name,
                'customer_name': customer_name,
                'customer_contact': customer_contact,
                'customer_location': customer_location,
                'items': items
            }

            if order['order_status'] == 'preparing':
                preparing_orders.append(order_data)
            elif order['order_status'] in ['serve', 'waiting for pickup']:
                serving_orders.append(order_data)

        return render_template(
            'kitchen_public_orderstatus_view.html',
            preparing_orders=preparing_orders,
            serving_orders=serving_orders
        )

    except Exception as e:
        print("Error loading order queue:", e)
        return render_template(
            'kitchen_public_orderstatus_view.html',
            preparing_orders=[],
            serving_orders=[]
        )

    finally:
        cursor.close()
        conn.close()


@kitchen_orderqueue_bp.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.get_json()
    order_id = data.get('order_id')

    if not order_id:
        return jsonify(success=False, message="Missing order_id"), 400

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Get the order_type for the given order
        cursor.execute("SELECT order_type FROM processing_orders WHERE order_ID = %s", (order_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify(success=False, message="Order not found"), 404

        order_type = result[0]

        # Set order_status based on order_type
        if order_type == 'delivery':
            new_status = 'waiting for pickup'
        else:
            new_status = 'served'

        # Update processing_orders table
        cursor.execute("""
            UPDATE processing_orders 
            SET order_status = %s 
            WHERE order_ID = %s
        """, (new_status, order_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True, message=f"Order status updated to '{new_status}'.")

    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

    

@kitchen_orderqueue_bp.route('/update_item_prep_status', methods=['POST'])
def update_item_prep_status():
    data = request.get_json()
    order_list_id = data.get('order_list_id')
    new_status = data.get('prep_status')

    if not order_list_id or not new_status:
        return jsonify(success=False, message="Missing order_list_id or prep_status"), 400

    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE processing_order_items
            SET Prep_status = %s
            WHERE order_list_ID = %s
        """, (new_status, order_list_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True, message="Prep status updated.")

    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@kitchen_orderqueue_bp.route('/api/kitchen_order_data')
def api_kitchen_order_data():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT order_ID, transaction_id, table_number, order_status, order_type,
                DATE_FORMAT(order_time, '%M %d %Y / %h:%i:%s %p') AS order_time, customer_id
            FROM processing_orders 
            WHERE order_status = 'pending'
            ORDER BY order_time DESC
        """)
        orders_data = cursor.fetchall()
        
        orders = []

        for order in orders_data:
            order_id = order['order_ID']
            cursor.execute("""
                SELECT order_list_ID, item_id, Item_Type, Quantity, Price_Per_Item, Total_Item_Price, Prep_status
                FROM processing_order_items 
                WHERE order_ID = %s
            """, (order_id,))
            raw_items = cursor.fetchall()

            items = []
            for item in raw_items:
                item_name = "UNKNOWN"
                item_type = item.get('Item_Type')
                item_id = item.get('item_id')

                if item_type == 'normal':
                    cursor.execute("SELECT Food_Name FROM food_list WHERE Food_ID = %s", (item_id,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result['Food_Name']
                elif item_type == 'dessert':
                    cursor.execute("SELECT Dessert_Name FROM dessert_list WHERE Dessert_ID = %s", (item_id,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result['Dessert_Name']
                elif item_type == 'drink':
                    cursor.execute("SELECT Drink_Name FROM drink_list WHERE Drink_ID = %s", (item_id,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result['Drink_Name']
                elif item_type == 'combo':
                    cursor.execute("SELECT Code_Name FROM combo_food_list WHERE Combo_List_ID = %s", (item_id,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result['Code_Name']

                item['Item_Name'] = item_name
                items.append(item)

            customer_id = order['customer_id']
            if customer_id:
                cursor.execute("""
                    SELECT CONCAT(ca.Lname, ', ', ca.Fname, ' ', ca.Mname) AS Customer_Name, 
                           ca.contact_number,
                           CONCAT(
                               cl.Street_Address, ', ',
                               cl.Barangay_Subdivision, ', ',
                               cl.City_Municipality, ', ',
                               cl.Province_Region, ' (Landmark: ',
                               cl.landmark, ')'
                           ) AS location
                    FROM customer_accounts ca
                    LEFT JOIN customer_locations cl ON ca.customer_id = cl.customer_id
                    WHERE ca.customer_id = %s
                """, (customer_id,))
                result = cursor.fetchone()
                customer_name = result['Customer_Name'] if result else "Unknown"
                customer_contact = result['contact_number'] if result else "Unknown"
                customer_location = result['location'] if result else "Unknown"
            else:
                customer_name = "Walk-In Guest"
                customer_contact = ""
                customer_location = ""

            orders.append({
                'order_id': order['order_ID'],
                'transaction_id': order['transaction_id'],
                'table_number': order['table_number'],
                'order_status': order['order_status'],
                'order_type': order['order_type'],
                'order_time': order['order_time'],
                'customer': customer_name,
                'customer_contact': customer_contact,
                'customer_location': customer_location,
                'items': items
            })

        return jsonify(orders=orders)

    except Exception as e:
        print("API error:", e)
        return jsonify(orders=[])

    finally:
        cursor.close()
        conn.close()