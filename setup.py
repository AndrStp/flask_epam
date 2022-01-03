#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup


setup(
    name='app',
    version='1.0.0',
    license='GNU General Public License v3',
    author='Andriy Stepanenko',
    author_email='ast.university@hotmail.com',
    description='Flask EDU Project for EPAM Python Winter School 2021',
    packages=['app'],
    platforms='any',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==2.0.2',
        'Flask-Login==0.5.0',
        'Flask-Mail==0.9.1',
        'Flask-Migrate==3.1.0',
        'Flask-RESTful==0.3.9',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-WTF==1.0.0',
        'psycopg2-binary==2.9.2',
        'pytest==6.2.5',
        'python-dotenv==0.19.2',
        'SQLAlchemy==1.4.27',
        'pylint==2.12.2',
    ]
)