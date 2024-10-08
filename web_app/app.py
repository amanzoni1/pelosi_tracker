from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

SUBSCRIBERS_FILE = os.path.join(os.path.dirname(__file__), 'subscribers.txt')
if not os.path.exists(SUBSCRIBERS_FILE):
    open(SUBSCRIBERS_FILE, 'w').close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # Add email to subscribers file
            with open(SUBSCRIBERS_FILE, 'a') as f:
                f.write(email + '\n')
            flash('Thank you for subscribing!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please enter a valid email address.', 'danger')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)