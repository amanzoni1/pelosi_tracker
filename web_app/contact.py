from flask import Blueprint, render_template, request, flash, redirect, url_for
from .forms import ContactForm 
from shared.emailer import send_contact_email

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        send_contact_email(name, email, message)

        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact.contact'))
    
    return render_template('contact.html', form=form)