from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Regexp, ValidationError
)
from shared.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$',
            message=(
                "Password must include at least: "
                "one uppercase letter, one lowercase letter, one number, "
                "and one special character (e.g., @, !, #)."
            )
        )
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message="Passwords must match.")
    ])
    
    submit = SubmitField('Register')

    # Custom validation to check if email already exists
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered. Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    submit = SubmitField('Reset Password')