from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db



auth = Blueprint('auth',__name__)

@auth.route('/login',methods = ['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in',category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Try again',category="error")
        else:
            flash("Email doesn't exist",category='error')
    return render_template('login.html',user=current_user)







@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))







@auth.route('/sign-up',methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Already a User",category='error')
        elif len(email)<4:
            flash('Email must be greater than 3', category='error')
        elif len(first_name)<2:
            flash('First Name must be greater than 2', category='error')
        elif len(password1) < 7:
            flash('Please use a longer password', category='error')
        elif len(password1)!=len(password2):
            flash('Password does not match', category='error')
        else:
            new_user  = User(email=email,first_name=first_name,password=generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user )
            db.session.commit()
            flash('Account Created', category='success')
            login_user(user,remember=True)
            return redirect(url_for('views.home'))
            # add user to database

    return render_template('sign-up.html',user=current_user)