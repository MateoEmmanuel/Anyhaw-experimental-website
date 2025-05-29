from flask import Flask, jsonify, render_template, request, url_for
from datetime import datetime
from collections import Counter
from data import user, orders_storage

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html', user=user)

@app.route('/menu')
def menu():
    orders = orders_storage

    # Define categories with their specific menu items
    categories = [
        {
            "title": "Best Sellers",
            "icon": url_for('static', filename='categoriesIcon/maincourse.png'),
            "menus": [
                {
                    "menu_title": "Litson Manok",
                    "menu_desc": "Jumbo Litson Manok",
                    "menu_price": 231.00,
                    "picture": url_for('static', filename='images/jumbow.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Litson Manok",
                    "menu_desc": "Regular Litson Manok",
                    "menu_price": 198.00,
                    "picture": url_for('static', filename='images/litson_manok.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Litson Manok",
                    "menu_desc": "Half Jumbo Litson Manok",
                    "menu_price": 121.00,
                    "picture": url_for('static', filename='images/half jumbo.jpg'),
                    "status": "available"
                }
            ]
        },
        {
            "title": "Others",
            "icon": url_for('static', filename='categoriesIcon/maincourse.png'),
            "menus": [
                {
                    "menu_title": "Liempo",
                    "menu_desc": "Delicous Any-Haw Liempo",
                    "menu_price": 176.00,
                    "picture": url_for('static', filename='images/liempo.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "CRISPY PATA",
                    "menu_desc": "Crispy Pork Pata",
                    "menu_price": 300.00,
                    "picture": url_for('static', filename='images/ypsirc atap.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Kare-Kare meal",
                    "menu_desc": "Delicous Kare-Kare with rice.",
                    "menu_price": 301.00,
                    "picture": url_for('static', filename='images/kare kare.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Plain Rice",
                    "menu_desc": "solo.",
                    "menu_price": 20.00,
                    "picture": url_for('static', filename='images/rice.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Valenciana",
                    "menu_desc": "solo.",
                    "menu_price": 60.00,
                    "picture": url_for('static', filename='images/valenciana.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "valenciana",
                    "menu_desc": "2 pc.",
                    "menu_price": 85.00,
                    "picture": url_for('static', filename='images/vlc.jpg'),
                    "status": "available"
                },
                 {
                    "menu_title": "chopsuey with rice",
                    "menu_desc": "2 - 3 persons.",
                    "menu_price": 130.00,
                    "picture": url_for('static', filename='images/chop 2-3.jpg'),
                    "status": "available"
                },
                 {
                    "menu_title": "chopsuey with rice",
                    "menu_desc": "6 - 8 persons.",
                    "menu_price": 250.00,
                    "picture": url_for('static', filename='images/chop 6-8.jpg'),
                    "status": "available"
                },
                 {
                    "menu_title": "kare kare with rice",
                    "menu_desc": "2 - 3 persons.",
                    "menu_price": 160.00,
                    "picture": url_for('static', filename='images/kare kare 2-3.jpg'),
                    "status": "available"
                },
                  {
                    "menu_title": "kare kare with rice",
                    "menu_desc": "6 - 8 persons.",
                    "menu_price": 310.00,
                    "picture": url_for('static', filename='images/kare kare 6-8.jpg'),
                    "status": "available"
                },
                 {
                    "menu_title": "chicharon bulaklak",
                    "menu_desc": "crispy chicharon bulaklak.",
                    "menu_price": 120.00,
                    "picture": url_for('static', filename='images/chicharonbulaklak.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "beef pares",
                    "menu_desc": "delicous beef pares.",
                    "menu_price": 85.00,
                    "picture": url_for('static', filename='images/beefpares.jpg'),
                    "status": "available"
                },
            ]
        },
        {
            "title": "Drinks",
            "icon": url_for('static', filename='categoriesIcon/milktea.png'),
            "menus": [
                {
                    "menu_title": "Buko Juice",
                    "menu_desc": "Buko Juice In Glass",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/coconut-inglass.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Buko Juice",
                    "menu_desc": "Buko Juice In Coconut Shell",
                    "menu_price": 60.00,
                    "picture": url_for('static', filename='images/coconut-shell.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Iced Tea",
                    "menu_desc": "Iced Tea In Glass",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/iced_teaglass.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Iced Tea",
                    "menu_desc": "Iced Tea In Pitcher",
                    "menu_price": 100.00,
                    "picture": url_for('static', filename='images/pitcher_icedtea.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Cucumber Lemonade",
                    "menu_desc": "Cucumber Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/cucumber_inglass.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Cucumber Lemonade",
                    "menu_desc": "Cucumber Lemonade In Pitcher",
                    "menu_price": 110.00,
                    "picture": url_for('static', filename='images/in_pitchercucumber.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Blue Lemonade",
                    "menu_desc": "Blue Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/bluelemonade_glass.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Blue Lemonade",
                    "menu_desc": "Blue Lemonade In Pitcher",
                    "menu_price": 110.00,
                    "picture": url_for('static', filename='images/bluelemonade_pitcher.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Pink Lemonade",
                    "menu_desc": "Pink Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/pink-lemonadeglass.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Sago't Gulaman",
                    "menu_desc": "Pink Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/sagot_gulamanglass.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Sago't Gulaman",
                    "menu_desc": "Sago't Gulaman In Pitcher",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/sagotgulaman_pitcher.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Black Gulaman",
                    "menu_desc": "Black Gulaman In Glass",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/blackgulaman.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Fruit Shake",
                    "menu_desc": "Refreshing Sweet Fruit Shake In Glass",
                    "menu_price": 70.00,
                    "picture": url_for('static', filename='images/fruitshake.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Buko Pandan Shake",
                    "menu_desc": "Refreshing Sweet Buko Pandan Shake In Glass",
                    "menu_price": 70.00,
                    "picture": url_for('static', filename='images/bukopandanshakee.jpg'),
                    "status": "available"
                },
            ]
        },
        {
            "title": "Combo Meals",
            "icon": url_for('static', filename='categoriesIcon/maincourse.png'),
            "menus": [
                {
                    "menu_title": "C1",
                    "menu_desc": "1 pc bbq, 1 pc valenciana 1 mismo.",
                    "menu_price": 95.00,
                    "picture": url_for('static', filename='images/c1.jpg'),
                    "status": "available"
                },
                
                {
                    "menu_title": "c2",
                    "menu_desc": "1 pc bbq, 1 pc valenciana, chopsuey, mismo.",
                    "menu_price": 120.00,
                    "picture": url_for('static', filename='images/c2.png'),
                    "status": "not available"
                },
                {
                    "menu_title": "c3",
                    "menu_desc": "1 qtr litson manok, 1 pc bbq, garlic rice, mismo.",
                    "menu_price": 120.00,
                    "picture": url_for('static', filename='images/c3.png'),
                    "status": "available"
                },
                {
                    "menu_title": "c4",
                    "menu_desc": "1 qtr litson manok, chopsuey, garlic rice, mismo.",
                    "menu_price": 125.00,
                    "picture": url_for('static', filename='images/c4.jpg'),
                    "status": "available"
                },
            ]
        },
        {
            "title": "Desserts",
            "icon": url_for('static', filename='categoriesIcon/frappe.png'),
            "menus": [
                {
                    "menu_title": "Leche Flan",
                    "menu_desc": "Creamy Leche Flan.",
                    "menu_price": 35.00,
                    "picture": url_for('static', filename='images/Leche_Flan.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Halo Halo Regular",
                    "menu_desc": "Refreshing regular Halo Halo with ice cream.",
                    "menu_price": 65.00,
                    "picture": url_for('static', filename='images/halohalowithicecream.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Halo Halo Special",
                    "menu_desc": "Refreshing Halo Halo special.",
                    "menu_price": 110.00,
                    "picture": url_for('static', filename='images/halohalospecial.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Buko Pandan",
                    "menu_desc": "Refreshing Buko Pandan.",
                    "menu_price": 110.00,
                    "picture": url_for('static', filename='images/bukopandandessert.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Fruit Salad",
                    "menu_desc": "Refreshing Fruit Salad.",
                    "menu_price": 110.00,
                    "picture": url_for('static', filename='images/fruitsalaad.jpg'),
                    "status": "not available"
                }
            ]
        },
        {
            "title": "Sizzling Meal",
            "icon": url_for('static', filename='categoriesIcon/maincourse.png'),
            "menus": [
                {
                    "menu_title": "Beef Sisig Kebab",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 100.00,
                    "picture": url_for('static', filename='images/beefsisigkebab.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Pork Sisig",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 85.00,
                    "picture": url_for('static', filename='images/porksisig.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Chicken Sisig",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 85.00,
                    "picture": url_for('static', filename='images/chickensisig.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Liempo",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 110.00,
                    "picture": url_for('static', filename='images/LIEMPOWW.jpg'),
                    "status": "not available"
                },
                   {
                    "menu_title": "Sizzling Porkchop",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 90.00,
                    "picture": url_for('static', filename='images/SIZZLING-PORKCHOP.jpg'),
                    "status": "not available"
                }, 
                   {
                    "menu_title": "Tenderloin",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 135.00,
                    "picture": url_for('static', filename='images/tenderloin.jpg'),
                    "status": "not available"
                },
                   {
                    "menu_title": "Boneless Bangus",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 135.00,
                    "picture": url_for('static', filename='images/boneless.jpg'),
                    "status": "not available"
                },
                 {
                    "menu_title": "Tanigue",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 115.00,
                    "picture": url_for('static', filename='images/tanigue.jpg'),
                    "status": "not available"
                },
            ]
        },
        {
            "title": "Silog",
            "icon": url_for('static', filename='categoriesIcon/maincourse.png'),
            "menus": [
                {
                    "menu_title": "Longsilog 2pcs",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 80.00,
                    "picture": url_for('static', filename='images/longsilog.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Hotsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": url_for('static', filename='images/hotsilog.jpg'),
                    "status": "available"
                },
                {
                    "menu_title": "Tapsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 90.00,
                    "picture": url_for('static', filename='images/tapsilog.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Cornsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": url_for('static', filename='images/cornsilog.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Porksilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 90.00,
                    "picture": url_for('static', filename='images/porksilog.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Liemposilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 110.00,
                    "picture": url_for('static', filename='images/liemposilog.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Baconsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 80.00,
                    "picture": url_for('static', filename='images/baconsilog.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Hamsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": url_for('static', filename='images/hamsilog.jpg'),
                    "status": "not available"
                },
                {
                    "menu_title": "Malingsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": url_for('static', filename='images/malingsilog.jpg'),
                    "status": "not available"
                },
                 {
                    "menu_title": "Chicksilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 95.00,
                    "picture": url_for('static', filename='images/chicksilog.jpg'),
                    "status": "not available"
                },
                 {
                    "menu_title": "Bangussilog Half",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 90.00,
                    "picture": url_for('static', filename='images/bangussilog.jpg'),
                    "status": "not available"
                }
            ]
        },
       
    ]

    # Dynamically create "All menu" category by aggregating all menus from other categories
    all_menus = []
    for category in categories:
        all_menus.extend(category["menus"])
    
    # Remove duplicates by menu_title and sort alphabetically
    unique_menus = {menu["menu_title"]: menu for menu in all_menus}
    all_menus = sorted(unique_menus.values(), key=lambda x: x["menu_title"])

    # Insert "All menu" category at the beginning
    categories.insert(0, {
        "title": "All menu",
        "icon": url_for('static', filename='categoriesIcon/allmenu.png'),
        "menus": all_menus
    })

    item_counts = Counter()
    for order in orders:
        total_items = sum(item["quantity"] for item in order.get("items", []))
        order["total_items"] = total_items
        for item in order.get("items", []):
            item_counts[item["ordername"]] += item["quantity"]

    item_summary = [{"ordername": item, "total_quantity": count} for item, count in item_counts.items()]

    return render_template('menu.html', orders=orders, item_summary=item_summary, categories=categories, user=user)

@app.route('/products')
def products():
    return render_template('products.html', user=user)

@app.route('/orders')
def orders():
    orders = orders_storage
    processed_orders = []
    
    # Validate data to prevent None, non-numeric, or non-iterable issues
    for order in orders:
        # Ensure order is a dictionary
        if not isinstance(order, dict):
            continue
            
        # Get items list first and ensure it's a list
        items_list = []
        if 'items' in order and isinstance(order['items'], list):
            items_list = order['items']
            
        # Convert order to a new dictionary to avoid modifying the original
        processed_order = {
            'id': str(order.get('id', '')),
            'customer_name': str(order.get('customer_name', 'Unknown')),
            'customer_table': str(order.get('customer_table', 'N/A')),
            'status': str(order.get('status', 'unknown')),
            'total': float(order.get('total', 0.0)),
            'total_items': int(order.get('total_items', 0)),
            'items': []
        }
        
        # Process items
        for item in items_list:
            if isinstance(item, dict):
                processed_item = {
                    'ordername': str(item.get('ordername', 'Unknown')),
                    'quantity': int(item.get('quantity', 0)),
                    'price': float(item.get('price', 0.0)),
                    'image': str(item.get('image', '')),
                    'comment': str(item.get('comment', ''))
                }
                processed_order['items'].append(processed_item)
        
        # Format created_at date
        created_at = order.get('created_at')
        if isinstance(created_at, str):
            try:
                date = datetime.fromisoformat(created_at)
                processed_order['created_at'] = date.strftime('%b %d, %Y %I:%M %p')
            except ValueError:
                processed_order['created_at'] = 'Invalid date'
        elif isinstance(created_at, datetime):
            processed_order['created_at'] = created_at.strftime('%b %d, %Y %I:%M %p')
        else:
            processed_order['created_at'] = 'Invalid date'
            
        processed_orders.append(processed_order)

    return render_template('orders.html', user=user, orders=processed_orders)

@app.route('/debug/orders')
def debug_orders():
    # Return raw orders_storage for debugging
    return jsonify(orders_storage)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=user)

@app.route('/settings')
def settings():
    return render_template('settings.html', user=user)

@app.route('/profile')
def profile():
    return render_template('profile.html', user=user)

@app.route('/api/greet')
def greet_json():
    name = request.args.get('name', 'Guest')
    return jsonify({
        'message': f'Hello {name}!',
        'status': 'success'
    })

@app.route('/greet')
def greet_page():
    return render_template('dashboard.html', user=user)

@app.route('/api/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['customerName', 'customerId', 'orderType', 'paymentMethod', 'cartItems', 'total', 'created_at']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Validate cartItems is a list
    if not isinstance(data.get('cartItems'), list):
        return jsonify({'error': 'cartItems must be a list'}), 400

    # Generate a new order ID
    new_id = f"#{(max(int(o['id'].lstrip('#')) for o in orders_storage) + 1) if orders_storage else 51240}"
    
    # Create the new order
    new_order = {
        "id": new_id,
        "customer_name": data['customerName'],
        "customer_table": "Table N/A" if data['orderType'].lower() == 'to-go' else f"Table {len(orders_storage) + 1}",
        "status": "waiting",
        "order_type": data['orderType'].capitalize(),
        "items": [
            {
                "ordername": item.get('title', 'Unknown'),
                "quantity": int(item.get('quantity', 0)),
                "price": float(item.get('price', 0.0)),
                "image": item.get('image', '')
            } for item in data['cartItems']
        ],
        "total": float(data.get('total', 0.0)),
        "created_at": datetime.fromisoformat(data['created_at']).isoformat(),
        "total_items": sum(int(item.get('quantity', 0)) for item in data['cartItems'])
    }

    # Add the new order to storage
    orders_storage.append(new_order)
    print(f"New order added: {new_order}")  # Debug output
    return jsonify({'message': 'Order placed successfully!', 'order_id': new_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)