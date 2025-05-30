from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for
from functools import wraps
from ..dbconnection import create_connection

delivery_bp = Blueprint('delivery_bp', __name__)

def delivery_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'role' not in session or session['role'] != 'delivery':
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@delivery_bp.route('/check-auth', methods=['GET'])
def check_auth():
    authenticated = 'user_id' in session and 'role' in session
    return jsonify({
        'authenticated': authenticated,
        'role': session.get('role', None)
    })

@delivery_bp.route('/active', methods=['GET'])
@delivery_required
def get_active_deliveries():
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                o.id as orderId,
                o.delivery_address as address,
                c.name as customerName,
                c.contact_number as customerPhone,
                o.status,
                o.total_amount,
                o.created_at
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.delivery_type = 'delivery'
            AND o.status IN ('preparing', 'out_for_delivery')
            AND (o.assigned_delivery_id = %s OR o.assigned_delivery_id IS NULL)
            ORDER BY o.created_at ASC
        """, (session['user_id'],))
        
        deliveries = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(deliveries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_bp.route('/history', methods=['GET'])
@delivery_required
def get_delivery_history():
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                o.id as orderId,
                o.delivery_address as address,
                c.name as customerName,
                o.status,
                o.completed_at as deliveredAt,
                o.total_amount
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.delivery_type = 'delivery'
            AND o.status = 'completed'
            AND o.assigned_delivery_id = %s
            ORDER BY o.completed_at DESC
            LIMIT 50
        """, (session['user_id'],))
        
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_bp.route('/update-location', methods=['POST'])
@delivery_required
def update_location():
    try:
        location = request.json
        if not location or 'lat' not in location or 'lng' not in location:
            return jsonify({"error": "Invalid location data"}), 400
            
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE delivery_locations
            SET 
                latitude = %s,
                longitude = %s,
                last_updated = CURRENT_TIMESTAMP
            WHERE delivery_id = %s
        """, (location['lat'], location['lng'], session['user_id']))
        
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO delivery_locations (delivery_id, latitude, longitude)
                VALUES (%s, %s, %s)
            """, (session['user_id'], location['lat'], location['lng']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Location updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@delivery_required
def update_order_status(order_id):
    try:
        status = request.json.get('status')
        if not status or status not in ['out_for_delivery', 'completed']:
            return jsonify({"error": "Invalid status"}), 400
            
        conn = create_connection()
        cursor = conn.cursor()
        
        if status == 'completed':
            cursor.execute("""
                UPDATE orders
                SET 
                    status = %s,
                    completed_at = CURRENT_TIMESTAMP
                WHERE id = %s AND assigned_delivery_id = %s
            """, (status, order_id, session['user_id']))
        else:
            cursor.execute("""
                UPDATE orders
                SET status = %s
                WHERE id = %s AND assigned_delivery_id = %s
            """, (status, order_id, session['user_id']))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Order not found or not assigned to you"}), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Order status updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_bp.route('/delivery_loader')
def delivery_loader():
    # Check if user is authenticated and has delivery role
    if 'user_id' in session and 'role' in session and session['role'] == 'delivery':
        return render_template("delivery/delivery_index.html")
    else:
        # Redirect to login if not authenticated or not a delivery person
        return redirect(url_for("Index_home"))
        
@delivery_bp.route('/get_delivery_info')
def get_delivery_info():
    # Example endpoint for fetching delivery information
    if 'user_id' not in session or session['role'] != 'delivery':
        return jsonify({"error": "Unauthorized"}), 403
        
    # Here you would typically fetch delivery data from database
    # For now returning placeholder data
    return jsonify({
        "success": True,
        "delivery_id": session.get('user_id'),
        "name": "Delivery User"
    }) 