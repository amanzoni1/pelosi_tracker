# web_app/app.py

import os
import sys

# Adjust the path to include the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, render_template, request, make_response, jsonify
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
import json
from datetime import datetime

from shared.extensions import db, bcrypt
from shared.models import User
from shared.utils import FLASK_SECRET_KEY, DATABASE_URL

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secure Cookie Settings
app.config['SESSION_COOKIE_SECURE'] = True     # Ensure cookies are only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True   # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Control cross-site sending of cookies

db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Import blueprints
from .auth import auth_bp
from .payment import payment_bp

app.register_blueprint(auth_bp)
app.register_blueprint(payment_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/set_cookie_preferences', methods=['POST'])
def set_cookie_preferences():
    preferences = request.json.get('preferences', {})
    response = make_response(jsonify({'message': 'Preferences saved'}))
    # Save preferences in a cookie (you may want to encrypt this)
    response.set_cookie(
        'cookie_preferences',
        json.dumps(preferences),
        secure=True,
        httponly=True,
        samesite='Lax'
    )
    return response

@app.context_processor
def inject_cookie_preferences():
    cookie_preferences = request.cookies.get('cookie_preferences')
    if cookie_preferences:
        preferences = json.loads(cookie_preferences)
    else:
        preferences = {}
    return dict(cookie_preferences=preferences)

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)