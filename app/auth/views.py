from flask import render_template, url_for, redirect, request, abort, flash
from flask_login import login_user, current_user, login_required
from flask_login.utils import logout_user
from . import auth
from ..service.service import UserService
from .forms import LoginForm, SignUpForm
from .email import send_mail


@auth.before_app_request
def before_request():
    """Catches requests of signed up yet uncofirmed users"""
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static' \
        and request.endpoint != 'main.index':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    form = LoginForm()
    if form.validate_on_submit():
        
        user = UserService.get_by_field(email=form.email.data)
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
    """Logout route"""
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Registration route"""
    form = SignUpForm()
    if form.validate_on_submit():
        user = UserService.create(email=form.email.data,
                                  username=form.username.data,
                                  password=form.password.data)
        token = user.generate_confirmation_token()
        send_mail(user.email, 
                  'Confirmation Letter', 
                  'auth/confirm',
                  user=user,
                  token=token)
        flash('A confirmation letter has been sent to you by email', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token: str):
    """Registration confirmation route"""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account', 'success')
    else:
        flash('The confirmation link is invalid or has expired', 'danger')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """Resends registration letter with new token"""
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 
              'Confirm your Account',
              'auth/confirm',
              user=current_user,
              token=token)
    flash('A new confirmation letter has been sent to your email', 'info')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    """Route for signed up yet unconfirmed users"""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html', title='Unconfirmed')