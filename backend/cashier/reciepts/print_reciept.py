import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32api
import win32print
from backend.dbconnection import create_connection
from datetime import datetime
import time

def parse_money(value):
    try:
        if isinstance(value, str):
            value = value.replace("₱", "").replace(",", "").strip()
        return float(value)
    except Exception:
        return 0.00

def print_receipt_by_order_id(or_logs_id,amount_paid,change_amount):
    # Connect to DB
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Get order info
    cursor.execute("""
        SELECT ol.Or_Logs_ID, ol.Transaction_ID, 
            CASE 
                WHEN ol.customer_id IS NULL THEN 'Walk-in Guest'
                ELSE CONCAT(ca.Lname, ', ', ca.Fname, ' ', ca.Mname) 
            END AS customer_name,
            ol.Date_Time, ol.Total_Price, ol.payment_method, 
            ol.Original_Price, ol.order_type,
            dt.Discount_Name,
            dt.Discount_Percent
        FROM Ordered_Logs ol
        LEFT JOIN customer_accounts ca ON ol.customer_id = ca.customer_id
        LEFT JOIN Discount_Table dt ON ol.Discount_ID = dt.Discount_ID
        WHERE ol.Or_Logs_ID = %s
    """, (or_logs_id,))
    order = cursor.fetchone()

    if not order:
        print("Order not found.")
        return

    # Get ordered items
    cursor.execute("""
       SELECT 
            CASE 
                WHEN oi.Item_Type = 'combo' THEN cf.Code_Name
                WHEN oi.Item_Type = 'drink' THEN d.Drink_Name
                WHEN oi.Item_Type = 'dessert' THEN ds.Dessert_Name
                ELSE fl.Food_Name
            END AS Item_Name,
            oi.Quantity,
            oi.Price_Per_Item
        FROM Ordered_Items oi
        LEFT JOIN Normal_Food_List nf 
            ON oi.Item_Type = 'normal' AND nf.food_id = oi.item_id
        LEFT JOIN Food_List fl 
            ON oi.Item_Type = 'normal' AND nf.Food_ID = fl.Food_ID
        LEFT JOIN Drink_List d 
            ON oi.Item_Type = 'drink' AND d.drink_id = oi.item_id
        LEFT JOIN Dessert_List ds 
            ON oi.Item_Type = 'dessert' AND ds.dessert_id = oi.item_id
        LEFT JOIN Combo_Food_List cf 
            ON oi.Item_Type = 'combo' AND cf.Combo_List_ID = oi.item_id
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
        draw_line(f"Customer: {order['customer_name']}")
        draw_line("!!!! DO NOT THROW CARELESSLY !!!!", bold=True)

    draw_line("-" * 40)

    for item in items:
        price = parse_money(item["Price_Per_Item"])  # Strip ₱ if needed
        total = item["Quantity"] * price
        draw_line(f"{item['Item_Name']} - {item['Quantity']} x ₱{price:.2f} = ₱{total:.2f}")



    draw_line("-" * 40)
    draw_line(f"Total: ₱{float(order['Total_Price']):.2f}", bold=True)

    if order["payment_method"] == "cash":
        if order.get("Discount_Name"):
            discount_name = order["Discount_Name"]
            discount_percent = float(order["Discount_Percent"]) * 100  # convert to percentage
            orig_price = parse_money(order["Original_Price"])
            final_price = parse_money(order["Total_Price"])
            discounted_amount = orig_price - final_price
            draw_line(f"Discount Applied: {discount_name} ({discount_percent:.0f}%) - ₱{discounted_amount:.2f}")

        
        amount = parse_money(amount_paid)
        draw_line(f"Amount Paid: ₱{amount:.2f}")
        
        change = parse_money(change_amount)
        draw_line(f"Change: ₱{change:.2f}")


    elif order["payment_method"] == "online":
        if order.get("Discount_Name"):
            discount_name = order["Discount_Name"]
            discount_percent = float(order["Discount_Percent"]) * 100  # convert to percentage
            orig_price = parse_money(order["Original_Price"])
            final_price = parse_money(order["Total_Price"])
            discounted_amount = orig_price - final_price
            draw_line(f"Discount Applied: {discount_name} ({discount_percent:.0f}%) - ₱{discounted_amount:.2f}")


    draw_line("")
    draw_line("Thank you for your order!")
    draw_line("www.anyhaw-litsonmanok.com")

    filename = os.path.join(os.getcwd(), "receipt_output.pdf")

    # Finalize the PDF
    c.save()

    # ✅ Wait for file write to complete
    time.sleep(1)

    # ✅ Confirm file exists and is accessible
    if not os.path.exists(filename):
        print("PDF file does not exist!")
    else:
        print("PDF exists:", filename)
        try:
            # Try opening to ensure it's not locked or corrupted
            with open(filename, 'rb') as f:
                f.read(1)

            # ✅ Get default printer and print
            printer_name = win32print.GetDefaultPrinter()
            print("Sending to printer:", printer_name)
            win32api.ShellExecute(0, "print", filename, None, ".", 0)

        except Exception as e:
            print("Error preparing or printing file:", e)


# --------------------------------------------------------------------------------------------------------------------------------------------------------
# reciept for delivery
def print_delivery_receipt(or_logs_id):
    # Connect to DB
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Get order info
    cursor.execute("""
        SELECT ol.Or_Logs_ID, ol.Transaction_ID, 
            CASE 
                WHEN ol.customer_id IS NULL THEN 'Walk-in Guest'
                ELSE CONCAT(ca.Lname, ', ', ca.Fname, ' ', ca.Mname) 
            END AS customer_name,
            ol.Date_Time, ol.Total_Price, ol.payment_method, 
            ol.Original_Price, ol.order_type,
            dt.Discount_Name,
            dt.Discount_Percent
        FROM Ordered_Logs ol
        LEFT JOIN customer_accounts ca ON ol.customer_id = ca.customer_id
        LEFT JOIN Discount_Table dt ON ol.Discount_ID = dt.Discount_ID
        WHERE ol.Or_Logs_ID = %s
    """, (or_logs_id,))
    order = cursor.fetchone()

    if not order:
        print("Order not found.")
        return

    # Get ordered items
    cursor.execute("""
        SELECT 
            CASE 
                WHEN oi.Item_Type = 'combo' THEN cf.Code_Name
                WHEN oi.Item_Type = 'drink' THEN d.Drink_Name
                WHEN oi.Item_Type = 'dessert' THEN ds.Dessert_Name
                ELSE fl.Food_Name
            END AS Item_Name,
            oi.Quantity,
            oi.Price_Per_Item
        FROM Ordered_Items oi
        LEFT JOIN Normal_Food_List nf 
            ON oi.Item_Type = 'normal' AND nf.food_id = oi.item_id
        LEFT JOIN Food_List fl 
            ON oi.Item_Type = 'normal' AND nf.Food_ID = fl.Food_ID
        LEFT JOIN Drink_List d 
            ON oi.Item_Type = 'drink' AND d.drink_id = oi.item_id
        LEFT JOIN Dessert_List ds 
            ON oi.Item_Type = 'dessert' AND ds.dessert_id = oi.item_id
        LEFT JOIN Combo_Food_List cf 
            ON oi.Item_Type = 'combo' AND cf.combo_id = oi.item_id
        WHERE oi.Or_Logs_ID = %s
    """, (or_logs_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    # Create PDF using reportlab
    filename = os.path.join(os.getcwd(), "delivery_receipt_output.pdf")
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
    draw_line(f"Customer: {order['customer_name']}")

    draw_line("-" * 40)

    for item in items:
        price = parse_money(item["Price_Per_Item"])
        total = item["Quantity"] * price
        draw_line(f"{item['Item_Name']} - {item['Quantity']} x ₱{price:.2f} = ₱{total:.2f}")

    draw_line("-" * 40)
    total_price = parse_money(order["Total_Price"])
    draw_line(f"Total: ₱{total_price:.2f}", bold=True)


    if order.get("Discount_Name"):
            discount_name = order["Discount_Name"]
            discount_percent = float(order["Discount_Percent"]) * 100  # convert to percentage
            orig_price = parse_money(order["Original_Price"])
            final_price = parse_money(order["Total_Price"])
            discounted_amount = orig_price - final_price
            draw_line(f"Discount Applied: {discount_name} ({discount_percent:.0f}%) - ₱{discounted_amount:.2f}")


    draw_line("")
    draw_line("Delivery Order - Please verify upon arrival.", bold=True)
    draw_line("Thank you for your order!")
    draw_line("www.anyhaw-litsonmanok.com")

    filename = os.path.join(os.getcwd(), "receipt_output.pdf")

    # Finalize the PDF
    c.save()

    # ✅ Wait for file write to complete
    time.sleep(1)

    # ✅ Confirm file exists and is accessible
    if not os.path.exists(filename):
        print("PDF file does not exist!")
    else:
        print("PDF exists:", filename)
        try:
            # Try opening to ensure it's not locked or corrupted
            with open(filename, 'rb') as f:
                f.read(1)

            # ✅ Get default printer and print
            printer_name = win32print.GetDefaultPrinter()
            print("Sending to printer:", printer_name)
            win32api.ShellExecute(0, "print", filename, None, ".", 0)

        except Exception as e:
            print("Error preparing or printing file:", e)
