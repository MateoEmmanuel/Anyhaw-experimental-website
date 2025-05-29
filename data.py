from datetime import datetime

# Mock user data
user = {
    "name": "Casey Kaspol",
    "role": "Cashier",
    "image": "images/user.png",
    "email": "casey.kaspol@example.com",
    "joined": "May 1, 2025"
}

# In-memory storage for orders (for demonstration purposes)
orders_storage = [
    {
        "id": "#51235",
        "customer_name": "John Doe",
        "customer_table": "Table 1",
        "status": "in progress",
        "order_type": "Dine In",
        "items": [
            {
                "ordername": "Classic Burger",
                "quantity": 2,
                "price": 329.45,
                "image": "images/menu_classicburger.jpg",
                "comment": "Extra cheese, no onions"
            },
            {
                "ordername": "Espresso",
                "quantity": 1,
                "price": 136.95,
                "image": "images/menu_espresso.png",
                "comment": "Double shot"
            },
            {
                "ordername": "Curly Fries",
                "quantity": 1,
                "price": 494.45,
                "image": "images/menu_curlyfries.jpg",
                "comment": "Extra crispy"
            }
        ],
        "total": 878.35,
        "created_at": datetime(2023, 10, 1, 12, 30).isoformat(),
        "total_items": 4
    },
    {
        "id": "#51236",
        "customer_name": "Jane Smith",
        "customer_table": "Table 2",
        "status": "completed",
        "order_type": "To Go",
        "items": [
            {
                "ordername": "Latte",
                "quantity": 3,
                "price": 136.95,
                "image": "images/menu_latte.png",
                "comment": "Extra hot, 2 sugars"
            },
            {
                "ordername": "Cheese Fries",
                "quantity": 1,
                "price": 494.45,
                "image": "images/menu_cheesefries.jpg",
                "comment": "Extra cheese sauce"
            }
        ],
        "total": 905.30,
        "created_at": datetime(2023, 10, 1, 13, 15).isoformat(),
        "total_items": 4
    },
    {
        "id": "#51237",
        "customer_name": "Bob Johnson",
        "customer_table": "Table 3",
        "status": "waiting",
        "order_type": "Dine In",
        "items": [
            {
                "ordername": "Cheeseburger",
                "quantity": 1,
                "price": 329.45,
                "image": "images/menu_cheeseburger.jpg",
                "comment": "No pickles, extra mayo"
            },
            {
                "ordername": "Cappuccino",
                "quantity": 2,
                "price": 136.95,
                "image": "images/menu_cappuccino.png",
                "comment": "Extra foam"
            }
        ],
        "total": 548.90,
        "created_at": datetime(2023, 10, 1, 14, 45).isoformat(),
        "total_items": 3
    },
    {
        "id": "#51238",
        "customer_name": "Alice Brown",
        "customer_table": "Table 4",
        "status": "canceled",
        "order_type": "To Go",
        "items": [
            {
                "ordername": "Sweet Potato Fries",
                "quantity": 2,
                "price": 494.45,
                "image": "images/menu_sweetpotatofries.jpg",
                "comment": "Extra seasoning"
            },
            {
                "ordername": "Mocha Frappe",
                "quantity": 1,
                "price": 136.95,
                "image": "images/menu_mochafrappe.jpg",
                "comment": "Extra whipped cream"
            }
        ],
        "total": 988.90,
        "created_at": datetime(2023, 10, 1, 15, 20).isoformat(),
        "total_items": 3
    },
    {
        "id": "#51239",
        "customer_name": "Charlie Green",
        "customer_table": "Table 5",
        "status": "in progress",
        "order_type": "Dine In",
        "items": [
            {
                "ordername": "Veggie Burger",
                "quantity": 1,
                "price": 329.45,
                "image": "images/menu_veggieburger.jpg",
                "comment": "No mushrooms"
            },
            {
                "ordername": "Caramel Frappe",
                "quantity": 1,
                "price": 136.95,
                "image": "images/menu_caramelfrappe.jpg",
                "comment": "Extra caramel drizzle"
            }
        ],
        "total": 466.40,
        "created_at": datetime(2023, 10, 1, 16, 10).isoformat(),
        "total_items": 2
    }
]