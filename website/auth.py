
from flask import Blueprint, render_template, request, flash, redirect, url_for,current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
import os

# create a blueprint
auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = '/path/to/the/uploads'




@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home_page'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        dob = request.form.get('Dateofbirth')
        uploaded_file = request.files['formFile']

        

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif uploaded_file.filename == '':
            flash('upload profile pic', category='error')
        else:
            uploaded_file.save(os.path.join("website/static/imgs/profileimgs/", uploaded_file.filename))
            new_user = User(username=username,email=email, password=generate_password_hash(
                password1, method='sha256'),dob=dob,profileImg=uploaded_file.filename)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect('/')

    return render_template('sign_up.html', user=current_user)
