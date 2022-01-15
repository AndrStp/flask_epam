from flask import render_template, url_for, redirect, request, flash, \
    current_app
from flask_login import login_user, current_user, login_required
from flask_login.utils import logout_user
from . import auth_bp
from ..service.service import UserService
from .forms import LoginForm, SignUpForm
from .email import send_mail


@auth_bp.before_app_request
def before_request():
    """Catches requests of signed up yet uncofirmed users"""
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static' \
        and request.endpoint != 'main.index':
        return redirect(url_for('auth.unconfirmed'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    form = LoginForm()
    if form.validate_on_submit():
        
        user = UserService.get_by_field(email=form.email.data)
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You have logged in', 'success')
            current_app.logger.debug(f'User: \'{user.username}\' has loged in')

            next_ = request.args.get('next')
            if not next_ or not next_.startswith('/'):
                next_ = url_for('main.dashboard')
            return redirect(next_)
        flash('Invalid credentials. Please check your email and password', 'danger')
    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    user = current_user._get_current_object()
    logout_user()
    flash('You have logged out', 'success')
    current_app.logger.debug(f'User: \'{user.username}\' has loged out')
    return redirect(url_for('main.index'))


@auth_bp.route('/signup', methods=['GET', 'POST'])
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
        current_app.logger.debug(f'User: \'{user.username}\' has signed up')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token: str):
    """Registration confirmation route"""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account', 'success')
        current_app.logger.debug(f'User: \'{current_user.username}\' has '\
            'confirmed mail account')
    else:
        flash('The confirmation link is invalid or has expired', 'danger')
    return redirect(url_for('main.index'))


@auth_bp.route('/confirm')
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
    current_app.logger.debug(f'User: \'{current_user.username}\' has requested '\
        'new confirmation token')
    return redirect(url_for('main.index'))


@auth_bp.route('/unconfirmed')
def unconfirmed():
    """Route for signed up yet unconfirmed users"""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html', title='Unconfirmed')
