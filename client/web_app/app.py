# client/web_app/app.py

import os
import sys

# Adjust the path to include the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate

from shared.extensions import db, bcrypt
from shared.models import User
from shared.utils import FLASK_SECRET_KEY, DATABASE_URL

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Import blueprints
from auth import auth_bp
from payment import payment_bp

app.register_blueprint(auth_bp)
app.register_blueprint(payment_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)