# web_app/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required
from extensions import db, bcrypt
from utils import SECRET_KEY, DATABASE_URL, FLASK_SECRET_KEY

from models import User

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)