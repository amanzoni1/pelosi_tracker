import os
import sys
import requests
import logging

logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)

# Adjust the path to include the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from shared.models import User
from shared.extensions import db
from datetime import datetime, timedelta
from shared.emailer import send_purchase_email
from shared.utils import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/payment-options', methods=['GET'])
@login_required
def payment_options():
    return render_template('payment_options.html', paypal_client_id=PAYPAL_CLIENT_ID)

def get_paypal_access_token():
    PAYPAL_OAUTH_API = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    # PAYPAL_OAUTH_API = "https://api-m.paypal.com/v1/oauth2/token"
    auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(PAYPAL_OAUTH_API, headers=headers, data=data, auth=auth)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        error_info = response.json()
        logger.error(f"Failed to get access token: {error_info}")
        raise Exception(f"Could not get access token from PayPal: {error_info.get('error_description', 'Unknown error')}")
    
@payment_bp.route('/create-order', methods=['POST'])
@login_required
def create_order():
    try:
        access_token = get_paypal_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        order_payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": "9.99"
                },
                "description": "1-year subscription to PoliticianTrade",
            }],
            "application_context": {
                "brand_name": "PoliticianTrade",
                "landing_page": "NO_PREFERENCE",
                "user_action": "PAY_NOW",
                "shipping_preference": "NO_SHIPPING"
            }
        }
        create_order_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        # create_order_url = "https://api-m.paypal.com/v2/checkout/orders"

        response = requests.post(create_order_url, headers=headers, json=order_payload)
        if response.status_code == 201:
            order = response.json()
            return jsonify({'id': order['id']})
        else:
            return jsonify({'error': response.json()}), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during order creation: {e}")
        return jsonify({'error': 'Network error occurred while creating the order.'}), 500
    except Exception as e:
        logger.exception("Unexpected error during order creation.")
        return jsonify({'error': 'An unexpected error occurred while creating the order.'}), 500

@payment_bp.route('/capture-order', methods=['POST'])
@login_required
def capture_order():
    order_id = request.json.get('orderID')
    if not order_id:
        return jsonify({'success': False, 'message': 'Order ID is missing.'}), 400
    try:
        access_token = get_paypal_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
        # capture_url = f"https://api-m.paypal.com/v2/checkout/orders/{order_id}/capture"
        response = requests.post(capture_url, headers=headers)
        if response.status_code in [200, 201]:
            capture_data = response.json()
            if capture_data['status'] == 'COMPLETED':
                # Update user's subscription status
                current_user.subscription_status = 'active'
                current_user.subscription_start = datetime.utcnow()
                current_user.subscription_end = current_user.subscription_start + timedelta(days=365)
                db.session.commit()

                send_purchase_email(current_user.email, current_user.email.split('@')[0])

                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Payment not completed.'}), 400
        else:
            error_message = response.json().get('message', 'Unknown error')
            return jsonify({'success': False, 'message': error_message}), response.status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@payment_bp.route('/cancel')
@login_required
def cancel():
    flash('Payment canceled.', 'info')
    return render_template('cancel.html')