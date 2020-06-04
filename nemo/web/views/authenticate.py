#!/usr/bin/env python3
#coding:utf-8

from flask import Blueprint, render_template, render_template_string, request, redirect, url_for, Flask, session
from instance import config
from functools import wraps

authenticate = Blueprint('authenticate', __name__)
ProductionConfig = config.ProductionConfig
app = Flask(__name__)
app.config.from_object(ProductionConfig)

@authenticate.route('/login', methods = ['POST','GET'])
def login_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if  password == app.config.get('WEB_PASSWORD'):
            try:
                session['login'] = 'A1akPTQJiz9wi9yo4rDz8ubM1b1'
                return redirect(url_for('index.view_index'))
            except Exception as e:
                print(e)

                return render_template('login.html', msg = 'Internal Server Error')
        else:
            return render_template('login.html', msg = 'Invalid Password')

    else:
        return render_template('login.html')

@authenticate.route('/logout', methods = ['GET'])
def logout():
    session['login'] = ''
    return redirect(url_for('authenticate.login_view'))

def login_check(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if session['login'] == 'A1akPTQJiz9wi9yo4rDz8ubM1b1':
                return f(*args, **kwargs)
            else:
                return redirect(url_for('authenticate.login_view'))
        except:
            return redirect(url_for('authenticate.login_view'))
    return wrapper


            
        