import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32api
import win32print
from backend.dbconnection import create_connection
from datetime import datetime

def print_receipt_by_order_id(or_logs_id):
    # Connect to DB
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Get order info
    cursor.execute("""
        SELECT ol.Or_Logs_ID, ol.Transaction_ID, 
                CONCAT(ca.Lname, ', ', ca.Fname, ' ', ca.Mname) AS Customer_Name, 
               ol.Date_Time, ol.Total_Price, ol.payment_method, 
               ol.gcash_ref, ol.order_type,
               ol.discount, ol.amount_paid, ol.change_amount
        FROM Ordered_Logs ol
        LEFT JOIN customer_accounts ca ON ol.customer_id = ca.customer_id
        WHERE ol.Or_Logs_ID = %s
    """, (or_logs_id,))
    order = cursor.fetchone()

    if not order:
        print("Order not found.")
        return

    if order["order_type"].lower() == "delivery":
        print("Delivery orders are excluded from printing.")
        return

    # Get ordered items
    cursor.execute("""
        SELECT 
            CASE 
                WHEN oi.Item_Type = 'combo' THEN cf.Combo_Name
                WHEN oi.Item_Type = 'drink' THEN d.Drink_Name
                WHEN oi.Item_Type = 'dessert' THEN ds.Dessert_Name
                ELSE nf.Food_Name
            END AS Item_Name,
            oi.Quantity,
            oi.Price_Per_Item
        FROM Ordered_Items oi
        LEFT JOIN Normal_Food_List nf ON oi.Item_Type = 'normal' AND nf.food_id = oi.item_id
        LEFT JOIN Drink_List d ON oi.Item_Type = 'drink' AND d.drink_id = oi.item_id
        LEFT JOIN Dessert_List ds ON oi.Item_Type = 'dessert' AND ds.dessert_id = oi.item_id
        LEFT JOIN Combo_Food_List cf ON oi.Item_Type = 'combo' AND cf.combo_id = oi.item_id
        WHERE oi.Or_Logs_ID = %s
    """, (or_logs_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    # Create PDF using reportlab
    filename = os.path.join(os.getcwd(), "receipt_output.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    y = height - 40
    line_height = 15

    def draw_line(text, bold=False):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 10)
        c.drawString(40, y, text)
        y -= line_height

    draw_line("Any-Haw Litson Manok", bold=True)
    draw_line(f"Order Type: {order['order_type'].capitalize()}")
    draw_line(f"Transaction ID: {order['Transaction_ID']}")
    draw_line(f"Order Time: {order['Date_Time'].strftime('%Y-%m-%d %H:%M:%S')}")
    if order["order_type"].lower() == "walk-in":
        draw_line(f"Customer: {order['customer_name'] or 'Guest'}")
        draw_line("!!!! DO NOT THROW CARELESSLY !!!!", bold=True)

    draw_line("-" * 40)

    for item in items:
        total = item["Quantity"] * item["Price_Per_Item"]
        draw_line(f"{item['Item_Name']} - {item['Quantity']} x ₱{item['Price_Per_Item']:.2f} = ₱{total:.2f}")

    draw_line("-" * 40)
    draw_line(f"Total: ₱{float(order['Total_Price']):.2f}", bold=True)

    if order["payment_method"] == "cash":
        draw_line(f"Discount: ₱{float(order.get('discount', 0.0)):.2f}")
        draw_line(f"Amount Paid: ₱{float(order.get('amount_paid', 0.0)):.2f}")
        draw_line(f"Change: ₱{float(order.get('change_amount', 0.0)):.2f}")
    elif order["payment_method"] == "online":
        draw_line(f"GCash Ref ID: {order.get('gcash_ref', '')}")

    draw_line("")
    draw_line("Thank you for your order!")
    draw_line("www.anyhaw-litsonmanok.com")

    c.save()

    # Print
    printer_name = win32print.GetDefaultPrinter()
    win32api.ShellExecute(0, "printto", filename, f'"{printer_name}"', ".", 0)
