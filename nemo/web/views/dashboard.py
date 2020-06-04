#!/usr/bin/env python3
#coding:utf-8


from collections import Counter
from flask import Blueprint, render_template
from .authenticate import login_check

from core.database.ip import Ip
from core.database.domain import Domain

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
#@login_check
def view_dashboard():
    ip_table = Ip()
    domain_table = Domain()
    dashboard_data = {
        'vul_count': 100,
        'plugin_count': 10,
        'week_passwd_count': 100,
        'server_count': ip_table.count()+domain_table.count()
    }
    return render_template('dashboard.html', dashboard_data = dashboard_data)
