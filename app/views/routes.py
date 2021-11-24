from flask import render_template, url_for, redirect, flash
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('auth/sign_in.html', title='Sign In', form=form)


@app.route('/sign_up')
def sign_up():
    return 'registration form'
