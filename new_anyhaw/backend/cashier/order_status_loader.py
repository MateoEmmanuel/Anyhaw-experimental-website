from flask import Blueprint, render_template, request, redirect, url_for
from backend.dbconnection import create_connection

cashier_orderstatus_bp = Blueprint('cashier_orderstatus', __name__, url_prefix='/cashier')

@cashier_orderstatus_bp.route('/order_status_loader')
def order_queue_loader():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get only 'Pending' orders including order_type and order_time
        cursor.execute("""
            SELECT order_ID, transaction_id, table_number, order_status, order_type, order_time 
            FROM processing_orders 
            WHERE order_status = 'preparing'
            ORDER BY order_ID DESC
        """)
        orders_data = cursor.fetchall()

        orders = []
        for order in orders_data:
            order_id = order['order_ID']

            # Get items in this order
            cursor.execute("""
                SELECT item_id, Item_Type, Quantity 
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
                'order_status': order['order_status'],
                'order_type': order['order_type'],
                'order_time': order['order_time'],
                'items': items
            })

        return render_template('cashier_orderstatus.html', orders=orders)

    except Exception as e:
        print("Error loading order queue:", e)
        return render_template('cashier_orderstatus.html', orders=[])

    finally:
        cursor.close()
        conn.close()

@cashier_orderstatus_bp.route('/update_orderstatus', methods=['POST'])
def update_orderstatus_serve():
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
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500
