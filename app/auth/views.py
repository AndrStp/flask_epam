from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, login_required
from flask_login.utils import logout_user
from . import auth
from app.models.user import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You have been logged in', 'success')

            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('main.dashboard')
            return redirect(next)
        flash('Invalid credentials. Please check your email and password', 'danger')
    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('auth/signup.html')