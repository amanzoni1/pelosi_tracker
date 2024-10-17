# shared/auth_utils.py

from itsdangerous import URLSafeTimedSerializer
from shared.utils import FLASK_SECRET_KEY

def generate_reset_token(email, expires_sec=1800):  # Expires in 30 minutes
    s = URLSafeTimedSerializer(FLASK_SECRET_KEY)
    return s.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expires_sec=1800):
    s = URLSafeTimedSerializer(FLASK_SECRET_KEY)
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expires_sec)
    except:
        return None
    return email