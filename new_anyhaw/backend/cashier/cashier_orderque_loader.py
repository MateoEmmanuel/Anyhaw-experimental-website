from flask import Blueprint, render_template
from backend.dbconnection import create_connection

cashier_orderqueue_bp = Blueprint('cashier_orderqueue', __name__, url_prefix='/cashier')

@cashier_orderqueue_bp.route('/order_queue_loader')
def order_queue_loader():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get only 'Pending' orders
        cursor.execute("""
            SELECT * FROM processing_orders 
            WHERE order_status = 'Pending'
            ORDER BY order_ID DESC
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
            items = cursor.fetchall()

            orders.append({
                'order_id': order['order_ID'],
                'transaction_id': order['transaction_id'],
                'table_number': order['table_number'],
                'order_status': order['order_status'],
                'items': items
            })

        return render_template('cashier_order_queue.html', orders=orders)

    except Exception as e:
        print("Error loading order queue:", e)
        return render_template('cashier_order_queue.html', orders=orders)

    finally:
        cursor.close()
        conn.close()
