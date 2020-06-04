#!/usr/bin/env python3
# coding:utf-8
from flask import Flask, render_template
from string import digits, ascii_lowercase
from random import sample
from .views.authenticate import authenticate
from .views.index import index
from .views.dashboard import dashboard
from .views.asset_manager import asset_manager
from .views.org_manager import org_manager
from .views.task_manager import task_manager

web_app = Flask(__name__)
#blueprint register
web_app.register_blueprint(authenticate)
web_app.register_blueprint(index)
web_app.register_blueprint(dashboard)
web_app.register_blueprint(asset_manager)
web_app.register_blueprint(org_manager)
web_app.register_blueprint(task_manager)