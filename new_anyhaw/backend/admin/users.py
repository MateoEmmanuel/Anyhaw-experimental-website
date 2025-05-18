from flask import render_template, redirect, url_for, request, session
from backend.dbconnection import get_db  # updated import
from . import admin_bp

@admin_bp.route('/users')
def users():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accounts WHERE role != 'admin'")
    users = cursor.fetchall()
    cursor.close()
    
    return render_template('admin_users.html', users=users)

@admin_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('admin.users'))
