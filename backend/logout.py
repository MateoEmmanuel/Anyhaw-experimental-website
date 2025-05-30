from flask import Blueprint, redirect, session, url_for

logout_bp = Blueprint('logout_bp', __name__)


@logout_bp.route('/logout', methods=['POST'])
def logout_sys():
    session.clear()
    return redirect(url_for('Index_home'))
