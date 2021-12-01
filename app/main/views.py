from flask import render_template, redirect, url_for, flash
from . import main


@main.route('/')
def index():
    return render_template('index.html', title='EDU Landing page')


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='dashboard')