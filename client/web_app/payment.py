# web_app/payment.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .models import User
from .extensions import db
import stripe
from .utils import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, WELCOME_TEMPLATE_ID
from datetime import datetime, timedelta
from .emailer import send_transactional_email


payment_bp = Blueprint('payment', __name__, url_prefix='/payment')
stripe.api_key = STRIPE_SECRET_KEY

@payment_bp.route('/subscribe', methods=['GET'])
@login_required
def subscribe():
    return render_template('payment.html', stripe_public_key=STRIPE_PUBLIC_KEY)

@payment_bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    domain_url = request.url_root
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Subscription',
                    },
                    'unit_amount': 899, 
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain_url + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + 'payment/cancel',
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403

@payment_bp.route('/success')
@login_required
def success():
    session_id = request.args.get('session_id')
    if not session_id:
        flash('Invalid session.', 'danger')
        return redirect(url_for('index'))

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        flash('Error retrieving payment session.', 'danger')
        return redirect(url_for('index'))

    if session.payment_status == 'paid':
        # Update user's subscription status
        current_user.subscription_status = 'active'
        current_user.subscription_start = datetime.utcnow()
        current_user.subscription_end = current_user.subscription_start + timedelta(days=365)  # Example: 30-day subscription
        db.session.commit()
        flash('Subscription successful!', 'success')

        # Send welcome email
        variables = {'user_name': current_user.email.split('@')[0]}
        send_transactional_email(current_user.email, WELCOME_TEMPLATE_ID, variables)

        return render_template('success.html')
    else:
        flash('Payment not completed.', 'danger')
        return redirect(url_for('index'))

@payment_bp.route('/cancel')
@login_required
def cancel():
    flash('Payment canceled.', 'info')
    return render_template('cancel.html')