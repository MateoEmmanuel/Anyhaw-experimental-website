from flask import render_template, redirect, url_for, request, session
from backend.dbconnection import get_db_connection
from . import admin_bp

@admin_bp.route('/menus')
def menus():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    conn.close()

    return render_template('admin_menus.html', menus=items)

@admin_bp.route('/delete_menu/<int:item_id>')
def delete_menu(item_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin.menus'))
