from flask import Blueprint, request, render_template
from shared.models import User
from shared.extensions import db

unsubscribe_bp = Blueprint('unsubscribe', __name__, url_prefix='/unsubscribe')

@unsubscribe_bp.route('/<email>', methods=['GET'])
def unsubscribe(email):
    user = User.query.filter_by(email=email).first()
    if user:
        user.is_subscribed_to_emails = False  
        db.session.commit()
        return render_template('unsubscribe_success.html', user=user)
    else:
        return render_template('unsubscribe_error.html', email=email)