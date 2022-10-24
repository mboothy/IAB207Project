
import email
from xmlrpc.client import boolean
from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from matplotlib.pyplot import get
from sqlalchemy import true
from werkzeug.security import generate_password_hash, check_password_hash
#from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db
from flask import Blueprint, render_template


# create a blueprint
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    form = RegisterForm()
    if request.method == 'POST':
        username = request.form, get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        Dateofbirth = request.form.get('Dateofbirth')
    return render_template("sign_up.html")


@auth.route('/Edit_profile')
def edit_profile_page():
    return render_template("edit_profile_page.html")


# this is the hint for a login function
# @bp.route('/login', methods=['GET', 'POST'])
# def authenticate(): #view function
#     print('In Login View function')
#     login_form = LoginForm()
#     error=None
#     if(login_form.validate_on_submit()==True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         u1 = User.query.filter_by(name=user_name).first()
#         if u1 is None:
#             error='Incorrect user name'
#         elif not check_password_hash(u1.password_hash, password): # takes the hash and password
#             error='Incorrect password'
#         if error is None:
#             login_user(u1)
#             nextp = request.args.get('next') #this gives the url from where the login page was accessed
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')
