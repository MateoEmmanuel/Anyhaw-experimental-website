from flask import Blueprint, render_template, request, jsonify
from backend.dbconnection import create_connection

cashier_delivery_status_loader_bp = Blueprint('cashier_delivery_status_loader', __name__, url_prefix='/cashier')

@cashier_delivery_status_loader_bp.route('/cashier_delivery_stats_loader')
def cashier_delivery_stats_loader():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get only 'Pending' orders including order_type and order_time
        cursor.execute("""
            SELECT 
                po.order_ID, 
                po.transaction_id, 
                po.table_number, 
                po.order_status, 
                po.order_type,
                DATE_FORMAT(po.order_time, '%M %d %Y / %h:%i:%s %p') AS order_time,
                po.customer_id,
                ol.status AS delivery_payment_status
            FROM processing_orders po
            JOIN Ordered_Logs ol ON po.transaction_id = ol.Transaction_ID
            WHERE po.order_status NOT IN ('pending')
            AND po.order_type = 'delivery'
            AND ol.status = 'unpaid'
            ORDER BY po.order_time DESC
        """)


        orders_data = cursor.fetchall()
        
        orders = []
        for order in orders_data:
            order_id = order['order_ID']

            # Get items in this order
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


            
        # Get customer names
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
            if result:
                customer_name = result['Customer_Name']
                customer_contact = result['contact_number']
                customer_location = result['location']

        # Append fully built order
        orders.append({
            'order_id': order['order_ID'],
            'transaction_id': order['transaction_id'],
            'table_number': order['table_number'],
            'order_status': order['order_status'],
            'order_type': order['order_type'],
            'order_time': order['order_time'],
            'customer_name': customer_name,
            'customer_contact': customer_contact,
            'customer_location': customer_location,
            'items': items,
            'status': order['delivery_payment_status']  # 'status' here is used for payment status
        })

        return render_template('Cashier_Delivery_status.html', orders=orders)

    except Exception as e:
        print("Error loading order queue:", e)
        return render_template('Cashier_Delivery_status.html', orders=[])

    finally:
        cursor.close()
        conn.close()
