import os
from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.models import User, Post 
from flaskblog import bcrypt, db
from .forms import (RegistrationForm, LoginForm, UpdateForm, 
                         RequestResetForm, ResetPasswordForm)
from .utils import save_picture, send_reset_email

users = Blueprint('users',__name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # h_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data
        )    
        db.session.add(user)
        db.session.commit()
        
        flash(f'Your account has been created! You are now able to loggin','success')
        return redirect(url_for('users.login'))
        
    return render_template("register.html", title = 'Register', form=form)

@users.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('main.home'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful ','success')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash(f'Login Unsuccessful, Please check your email and password ','danger')
    return render_template("login.html", title = 'Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form =  UpdateForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            filename = os.path.join('http://localhost:5000/static/images',picture_file)
            current_user.image_file = filename
    
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash(f'Account Updated successfully','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username 
    return render_template("account.html", title="Account", form = form, user = current_user)

@users.route('/view_profile/<string:username>')
def view_profile(username):
    form =  UpdateForm()
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page, per_page = 5)

    if current_user.is_anonymous:
        flash(f'You have to be logged in to view a user', 'info')
        return redirect(url_for('users.login'))
    
    if current_user.username == user.username:
        return redirect(url_for('users.account'))
            
    return render_template('account.html', user = user, title = 'view profile', posts = posts, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
           flash(f'You do not have an account or Enter a valid email', 'danger')
           return redirect(url_for('users.login'))
        send_reset_email(user)
        flash(f'An email has been sent with instruction to reset your password. ', 'success')
        return redirect(url_for('users.login'))
    
        # return redirect(url_for('home'))
    return render_template('reset_request.html', title = "Reset Password", form = form)

@users.route('/reset_password/<token>',methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    
    h_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user.password = h_password
    db.session.commit()
    flash(f'Password successfully reset')
    
    if user is None:
        flash(f'That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    return render_template("reset_token.html", title = 'Reset Password', form = form)