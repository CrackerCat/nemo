#!/usr/bin/env python3
#coding:utf-8

import json
import hashlib

from flask import Flask, request, url_for, render_template, Blueprint, redirect, render_template_string
from .authenticate import login_check
from core.database.organization import Organization

org_manager = Blueprint("org_manager", __name__)

@org_manager.route('/org-add', methods = ['GET', 'POST'])
#@login_check
def org_add_view():
    '''
        添加组织机构
    '''
    org_table = Organization()
    if request.method == 'POST':
        org_name = request.form['org_name'].encode('utf-8')
        org_hash = hashlib.md5(org_name).hexdigest()
        if not org_table.gets(query = {'sort_order': org_hash}):
            org_table.add(data = {
                'org_name': org_name,
                'status': 'enable' if request.form['status'] == '0' else 'disable',
                'sort_order': org_hash
            })

    return render_template('org-add.html')


@org_manager.route('/org-list', methods = ['GET', 'POST'])
#@login_check
def org_list_view():
    '''
        组织机构列表展示
    '''
    if request.method == 'GET':
        return render_template('org-list.html')

    org_table = Organization()
    org_list = []
    json_data = {}
    index = 1

    try:
        draw = int(request.form.get('draw'))
        start = int(request.form.get('start'))
        length = int(request.form.get('length'))
        search_key = request.form.get('search[value]')
        order_column = request.form.get('order[0][column]') 
        order_column = request.form.get('order[0][dir]')
        for org in org_table.gets(page = (start//length) + 1, rows_per_page = length):
            org_list.append({
                "id": org['id'],
                'index':index,
                'org_name': org['org_name'],
                'status': org['status'],
                'sort_order': org['sort_order'],
                'create_time': str(org['create_datetime']),
                'update_time': str(org['update_datetime'])
            })
            index += 1
        count = org_table.count()
        json_data = {
            'draw': draw,
            'recordsTotal': count,
            'recordsFiltered': count,
            'data': org_list,
        }
    except Exception as e:
        print(e)

    return render_template_string(json.dumps(json_data))