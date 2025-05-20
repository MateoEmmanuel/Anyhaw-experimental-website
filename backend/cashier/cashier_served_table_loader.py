from flask import Blueprint, render_template
from backend.dbconnection import create_connection

cashier_served_order_bp = Blueprint('served_order_loader', __name__)

@cashier_served_order_bp.route('/served_order_loader')
def served_order_loader():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get only 'Pending' orders including order_type and order_time
        cursor.execute("""
            SELECT order_ID, transaction_id, table_number, order_status, order_type, order_time,customer
            FROM processing_orders 
            WHERE order_status = 'served'
            AND order_type IN ('dine-in', 'take-out')
            ORDER BY order_time DESC;
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

            orders.append({
                'order_id': order['order_ID'],
                'transaction_id': order['transaction_id'],
                'table_number': order['table_number'],
                'order_time': order['order_time'],
                'customer': order['customer'],
                'order_status': order['order_status'],
                'order_type': order['order_type'],
                'items': items
            })

        return render_template('cashier_served_order.html', orders=orders)

    except Exception as e:
        print("Error loading order queue:", e)
        return render_template('cashier_served_order.html', orders=[])

    finally:
        cursor.close()
        conn.close()
