import os

# Path to the data.py file
file_path = 'new_anyhaw/data.py'

# Read the current content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Items to restore back to "not available"
items_to_restore = [
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
    
    # Other items that were changed
    '"menu_title": "Chicken Sisig"',
    '"menu_title": "Liempo"',
    '"menu_title": "Sizzling Porkchop"',
    '"menu_title": "c2"',
    '"menu_title": "Tapsilog"',
    '"menu_title": "Cornsilog"',
    '"menu_title": "Porksilog"',
    '"menu_title": "Chicksilog"'
]

# Update the status for each item
for item in items_to_restore:
    # Find the item and change its status to "not available"
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
                # Replace 'available' with 'not available'
                if 'available' in status_line and 'not available' not in status_line:
                    new_status_line = status_line.replace('"available"', '"not available"')
                    # Replace in the content
                    content = content[:status_pos] + new_status_line + content[end_status:]

# Write the updated content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("Menu items restored to original state successfully!") 