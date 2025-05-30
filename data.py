from datetime import datetime
from flask import url_for

# Mock user data
user = {
    "name": "Casey Kaspol",
    "role": "Cashier",
    "image": "images/user.png",
    "email": "casey.kaspol@example.com",
    "joined": "May 1, 2025"
}

# Menu data
menu_items = [
    {
        "id": "1",
        "name": "Chicken Inasal",
        "description": "Grilled chicken marinated in local spices",
        "price": 150.00,
        "image": "/static/assets/images/menu/inasal.jpg",
        "available": True
    },
    {
        "id": "2",
        "name": "Paa",
        "description": "Chicken leg quarter grilled to perfection",
        "price": 120.00,
        "image": "/static/assets/images/menu/paa.jpg",
        "available": True
    }
]

# Function to get categories with their menu items
def get_categories():
    categories = [
        {
            "title": "Best Sellers",
            "icon": "static/assets/images/categoriesIcon/maincourse.png",
            "menus": [
                {
                    "menu_title": "Litson Manok",
                    "menu_desc": "Jumbo Litson Manok",
                    "menu_price": 231.00,
                    "picture": "static/assets/images/menu/jumbow.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Litson Manok",
                    "menu_desc": "Regular Litson Manok",
                    "menu_price": 198.00,
                    "picture": "static/assets/images/menu/litson_manok.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Litson Manok",
                    "menu_desc": "Half Jumbo Litson Manok",
                    "menu_price": 121.00,
                    "picture": "static/assets/images/menu/half jumbo.jpg",
                    "status": "available"
                }
            ]
        },
        {
            "title": "Others",
            "icon": "static/assets/images/categoriesIcon/maincourse.png",
            "menus": [
                {
                    "menu_title": "Liempo",
                    "menu_desc": "Delicous Any-Haw Liempo",
                    "menu_price": 176.00,
                    "picture": "static/assets/images/menu/liempo.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "CRISPY PATA",
                    "menu_desc": "Crispy Pork Pata",
                    "menu_price": 300.00,
                    "picture": "static/assets/images/menu/ypsirc atap.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Kare-Kare meal",
                    "menu_desc": "Delicous Kare-Kare with rice.",
                    "menu_price": 301.00,
                    "picture": "static/assets/images/menu/kare kare.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Plain Rice",
                    "menu_desc": "solo.",
                    "menu_price": 20.00,
                    "picture": "static/assets/images/menu/rice.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Valenciana",
                    "menu_desc": "solo.",
                    "menu_price": 60.00,
                    "picture": "static/assets/images/menu/valenciana.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "valenciana",
                    "menu_desc": "2 pc.",
                    "menu_price": 85.00,
                    "picture": "static/assets/images/menu/vlc.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "chopsuey with rice",
                    "menu_desc": "2 - 3 persons.",
                    "menu_price": 130.00,
                    "picture": "static/assets/images/menu/chop 2-3.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "chopsuey with rice",
                    "menu_desc": "6 - 8 persons.",
                    "menu_price": 250.00,
                    "picture": "static/assets/images/menu/chop 6-8.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "kare kare with rice",
                    "menu_desc": "2 - 3 persons.",
                    "menu_price": 160.00,
                    "picture": "static/assets/images/menu/kare kare 2-3.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "kare kare with rice",
                    "menu_desc": "6 - 8 persons.",
                    "menu_price": 310.00,
                    "picture": "static/assets/images/menu/kare kare 6-8.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "chicharon bulaklak",
                    "menu_desc": "crispy chicharon bulaklak.",
                    "menu_price": 120.00,
                    "picture": "static/assets/images/menu/chicharonbulaklak.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "beef pares",
                    "menu_desc": "delicous beef pares.",
                    "menu_price": 85.00,
                    "picture": "static/assets/images/menu/beefpares.jpg",
                    "status": "available"
                }
            ]
        },
        {
            "title": "Drinks",
            "icon": "static/assets/images/categoriesIcon/milktea.png",
            "menus": [
                {
                    "menu_title": "Buko Juice",
                    "menu_desc": "Buko Juice In Glass",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/coconut-inglass.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Buko Juice",
                    "menu_desc": "Buko Juice In Coconut Shell",
                    "menu_price": 60.00,
                    "picture": "static/assets/images/menu/coconut-shell.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Iced Tea",
                    "menu_desc": "Iced Tea In Glass",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/iced_teaglass.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Iced Tea",
                    "menu_desc": "Iced Tea In Pitcher",
                    "menu_price": 100.00,
                    "picture": "static/assets/images/menu/pitcher_icedtea.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Cucumber Lemonade",
                    "menu_desc": "Cucumber Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/cucumber_inglass.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Cucumber Lemonade",
                    "menu_desc": "Cucumber Lemonade In Pitcher",
                    "menu_price": 110.00,
                    "picture": "static/assets/images/menu/in_pitchercucumber.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Blue Lemonade",
                    "menu_desc": "Blue Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/bluelemonade_glass.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Blue Lemonade",
                    "menu_desc": "Blue Lemonade In Pitcher",
                    "menu_price": 110.00,
                    "picture": "static/assets/images/menu/bluelemonade_pitcher.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Pink Lemonade",
                    "menu_desc": "Pink Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/pink-lemonadeglass.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Sago't Gulaman",
                    "menu_desc": "Pink Lemonade In Glass",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/sagot_gulamanglass.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Sago't Gulaman",
                    "menu_desc": "Sago't Gulaman In Pitcher",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/sagotgulaman_pitcher.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Black Gulaman",
                    "menu_desc": "Black Gulaman In Glass",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/blackgulaman.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Fruit Shake",
                    "menu_desc": "Refreshing Sweet Fruit Shake In Glass",
                    "menu_price": 70.00,
                    "picture": "static/assets/images/menu/fruitshake.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Buko Pandan Shake",
                    "menu_desc": "Refreshing Sweet Buko Pandan Shake In Glass",
                    "menu_price": 70.00,
                    "picture": "static/assets/images/menu/bukopandanshakee.jpg",
                    "status": "available"
                }
            ]
        },
        {
            "title": "Combo Meals",
            "icon": "static/assets/images/categoriesIcon/maincourse.png",
            "menus": [
                {
                    "menu_title": "C1",
                    "menu_desc": "1 pc bbq, 1 pc valenciana 1 mismo.",
                    "menu_price": 95.00,
                    "picture": "static/assets/images/menu/c1.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "c2",
                    "menu_desc": "1 pc bbq, 1 pc valenciana, chopsuey, mismo.",
                    "menu_price": 120.00,
                    "picture": "static/assets/images/menu/c2.png",
                    "status": "not available"
                },
                {
                    "menu_title": "c3",
                    "menu_desc": "1 qtr litson manok, 1 pc bbq, garlic rice, mismo.",
                    "menu_price": 120.00,
                    "picture": "static/assets/images/menu/c3.png",
                    "status": "available"
                },
                {
                    "menu_title": "c4",
                    "menu_desc": "1 qtr litson manok, chopsuey, garlic rice, mismo.",
                    "menu_price": 125.00,
                    "picture": "static/assets/images/menu/c4.jpg",
                    "status": "available"
                }
            ]
        },
        {
            "title": "Desserts",
            "icon": "static/assets/images/categoriesIcon/frappe.png",
            "menus": [
                {
                    "menu_title": "Leche Flan",
                    "menu_desc": "Creamy Leche Flan.",
                    "menu_price": 35.00,
                    "picture": "static/assets/images/menu/Leche_Flan.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Halo Halo Regular",
                    "menu_desc": "Refreshing regular Halo Halo with ice cream.",
                    "menu_price": 65.00,
                    "picture": "static/assets/images/menu/halohalowithicecream.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Halo Halo Special",
                    "menu_desc": "Refreshing Halo Halo special.",
                    "menu_price": 110.00,
                    "picture": "static/assets/images/menu/halohalospecial.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Buko Pandan",
                    "menu_desc": "Refreshing Buko Pandan.",
                    "menu_price": 110.00,
                    "picture": "static/assets/images/menu/bukopandandessert.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Fruit Salad",
                    "menu_desc": "Refreshing Fruit Salad.",
                    "menu_price": 110.00,
                    "picture": "static/assets/images/menu/fruitsalaad.jpg",
                    "status": "not available"
                }
            ]
        },
        {
            "title": "Sizzling Meal",
            "icon": "static/assets/images/categoriesIcon/maincourse.png",
            "menus": [
                {
                    "menu_title": "Beef Sisig Kebab",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 100.00,
                    "picture": "static/assets/images/menu/beefsisigkebab.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Pork Sisig",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 85.00,
                    "picture": "static/assets/images/menu/porksisig.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Chicken Sisig",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 85.00,
                    "picture": "static/assets/images/menu/chickensisig.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Liempo",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 110.00,
                    "picture": "static/assets/images/menu/LIEMPOWW.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Sizzling Porkchop",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 90.00,
                    "picture": "static/assets/images/menu/SIZZLING-PORKCHOP.jpg",
                    "status": "not available"
                }, 
                {
                    "menu_title": "Tenderloin",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 135.00,
                    "picture": "static/assets/images/menu/tenderloin.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Boneless Bangus",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 135.00,
                    "picture": "static/assets/images/menu/boneless.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Tanigue",
                    "menu_desc": "Served in hot plate.",
                    "menu_price": 115.00,
                    "picture": "static/assets/images/menu/tanigue.jpg",
                    "status": "not available"
                }
            ]
        },
        {
            "title": "Silog",
            "icon": "static/assets/images/categoriesIcon/maincourse.png",
            "menus": [
                {
                    "menu_title": "Longsilog 2pcs",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 80.00,
                    "picture": "static/assets/images/menu/longsilog.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Hotsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": "static/assets/images/menu/hotsilog.jpg",
                    "status": "available"
                },
                {
                    "menu_title": "Tapsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 90.00,
                    "picture": "static/assets/images/menu/tapsilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Cornsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": "static/assets/images/menu/cornsilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Porksilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 90.00,
                    "picture": "static/assets/images/menu/porksilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Liemposilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 110.00,
                    "picture": "static/assets/images/menu/liemposilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Baconsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 80.00,
                    "picture": "static/assets/images/menu/baconsilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Hamsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": "static/assets/images/menu/hamsilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Malingsilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 75.00,
                    "picture": "static/assets/images/menu/malingsilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Chicksilog",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 95.00,
                    "picture": "static/assets/images/menu/chicksilog.jpg",
                    "status": "not available"
                },
                {
                    "menu_title": "Bangussilog Half",
                    "menu_desc": "With egg and fried rice.",
                    "menu_price": 90.00,
                    "picture": "static/assets/images/menu/bangussilog.jpg",
                    "status": "not available"
                }
            ]
        }
    ]
    
    # Create "All menu" category by collecting all menus from other categories
    all_menus = []
    for category in categories:
        all_menus.extend(category["menus"])
    
    # Remove duplicates by menu_title and sort alphabetically
    unique_menus = {menu["menu_title"]: menu for menu in all_menus}
    all_menus = sorted(unique_menus.values(), key=lambda x: x["menu_title"])

    # Insert "All menu" category at the beginning
    categories.insert(0, {
        "title": "All menu",
        "icon": "static/assets/images/categoriesIcon/allmenu.png",
        "menus": all_menus
    })
    
    return categories

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
                "image": "static/assets/images/menu/menu_classicburger.jpg",
                "comment": "Extra cheese, no onions"
            },
            {
                "ordername": "Espresso",
                "quantity": 1,
                "price": 136.95,
                "image": "static/assets/images/menu/menu_espresso.png",
                "comment": "Double shot"
            },
            {
                "ordername": "Curly Fries",
                "quantity": 1,
                "price": 494.45,
                "image": "static/assets/images/menu/menu_curlyfries.jpg",
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
                "image": "static/assets/images/menu/menu_latte.png",
                "comment": "Extra hot, 2 sugars"
            },
            {
                "ordername": "Cheese Fries",
                "quantity": 1,
                "price": 494.45,
                "image": "static/assets/images/menu/menu_cheesefries.jpg",
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
                "image": "static/assets/images/menu/menu_cheeseburger.jpg",
                "comment": "No pickles, extra mayo"
            },
            {
                "ordername": "Cappuccino",
                "quantity": 2,
                "price": 136.95,
                "image": "static/assets/images/menu/menu_cappuccino.png",
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
                "image": "static/assets/images/menu/menu_sweetpotatofries.jpg",
                "comment": "Extra seasoning"
            },
            {
                "ordername": "Mocha Frappe",
                "quantity": 1,
                "price": 136.95,
                "image": "static/assets/images/menu/menu_mochafrappe.jpg",
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
                "image": "static/assets/images/menu/menu_veggieburger.jpg",
                "comment": "No mushrooms"
            },
            {
                "ordername": "Caramel Frappe",
                "quantity": 1,
                "price": 136.95,
                "image": "static/assets/images/menu/menu_caramelfrappe.jpg",
                "comment": "Extra caramel drizzle"
            }
        ],
        "total": 466.40,
        "created_at": datetime(2023, 10, 1, 16, 10).isoformat(),
        "total_items": 2
    }
] 