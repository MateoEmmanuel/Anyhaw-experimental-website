import os

# Path to the data.py file
file_path = 'new_anyhaw/data.py'

# Read the current content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Items to update status to "available"
items_to_update = [
    # Sizzling
    '"menu_title": "Tenderloin"',
    '"menu_title": "Boneless Bangus"',
    '"menu_title": "Tanigue"',
    
    # Silog
    '"menu_title": "Liemposilog"',
    '"menu_title": "Baconsilog"',
    '"menu_title": "Hamsilog"',
    '"menu_title": "Malingsilog"',
    '"menu_title": "Bangussilog Half"',
    
    # Dessert
    '"menu_title": "Halo Halo Special"',
    '"menu_title": "Buko Pandan"',
    '"menu_title": "Fruit Salad"',
    
    # Drinks (likely already available)
    '"menu_title": "Buko Juice"',
    '"menu_desc": "Buko Juice In Coconut Shell"',
    
    # Combo meals
    '"menu_title": "c3"',
    '"menu_title": "c4"',
    
    # Others
    '"menu_title": "Valenciana"',
    '"menu_desc": "solo."',
    '"menu_title": "valenciana"',
    '"menu_desc": "2 pc."',
    '"menu_title": "chopsuey with rice"',
    '"menu_desc": "2 - 3 persons."',
    '"menu_title": "chopsuey with rice"',
    '"menu_desc": "6 - 8 persons."',
    '"menu_title": "kare kare with rice"',
    '"menu_desc": "2 - 3 persons."',
    '"menu_title": "kare kare with rice"',
    '"menu_desc": "6 - 8 persons."',
    '"menu_title": "chicharon bulaklak"',
    '"menu_title": "beef pares"'
]

# Update the status for each item
for item in items_to_update:
    # Find the item and change its status to "available"
    # Look for the item followed by any text and then status field
    start_pos = content.find(item)
    if start_pos != -1:
        # Find the status field after the item
        status_pos = content.find('"status":', start_pos)
        if status_pos != -1:
            # Find the end of the status line
            end_status = content.find('\n', status_pos)
            if end_status != -1:
                # Extract the current status line
                status_line = content[status_pos:end_status]
                # Replace 'not available' with 'available'
                if 'not available' in status_line:
                    new_status_line = status_line.replace('"not available"', '"available"')
                    # Replace in the content
                    content = content[:status_pos] + new_status_line + content[end_status:]

# Write the updated content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("Menu items updated successfully!") 