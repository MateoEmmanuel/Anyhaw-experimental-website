from flask import Blueprint, render_template, send_file, redirect, url_for, session, jsonify
from backend.dbconnection import create_connection

cashier_system_bp = Blueprint('cashier_system_bp', __name__)

@cashier_system_bp.route('/cashier_system_loader')
def cashier_system_loader():
    return render_template('cashier_system.html')