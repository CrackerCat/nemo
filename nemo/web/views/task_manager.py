#!/usr/bin/env python3
#coding:utf-8

import json
import hashlib
import requests

from flask import Flask, request, url_for, render_template, Blueprint, redirect, render_template_string
from .authenticate import login_check
from core.database.organization import Organization
from core.database.ip import Ip
from core.database.domain import Domain
from core.tasks.taskapi import TaskAPI


task_manager = Blueprint("task_manager", __name__)

@task_manager.route('/task-add', methods = ['GET', 'POST'])
#@login_check
def task_add_view():
    '''
        添加任务
    '''
    taskapi = TaskAPI()
    ip_table = Ip()
    org_table = Organization()
    domain_table = Domain()

    if request.method == 'GET':
        
        return render_template('task-add.html', org_list = [(org_row['id'],org_row['org_name']) for org_row in org_table.gets()])
    #POST
    task_info = {
        'task_name': request.form.get('task_name'),
        'task_type': request.form.get('task_type'),
        'task_plan': request.form.get('task_plan'),
        'org_names': request.form.get('org_names'),
        'task_creator': request.form.get('task_creator')
    }
    print(task_info)
    #taskapi.start_task('iplocation',kwargs={'task_name':'get ip location','options':{'target':('218.19.148.193',)}})
    for org_id in task_info['org_names'].split(','):
        for task in task_info['task_type'].split(','):
            targets = []
            options = {}
            for domain_row in domain_table.gets(query = {'org_id': org_id}):
                targets.append(domain_row['domain'])
            for ip_row in ip_table.gets(query = {'org_id': org_id}):
                targets.append(ip_row['ip'])
            if not targets:
                continue
            if task == 'nmap':
                options['port'] = '--top 1000'
                options['ping'] = False
                options['tech'] = 'sT'
            elif task == 'portscan':
                options['port'] = '80,8080,443'
                options['org_id'] = int(org_id)
                options['webtitle'] = True
                options['iplocation'] = True

            options['target'] = targets
            
            result = taskapi.start_task(task.strip(), kwargs = {'task_name': task_info['task_name'], 'options':options})
            print(result)

    return render_template('task-add.html', asset_list = 'aaaaaaaa')


@task_manager.route('/task-list', methods = ['GET', 'POST'])
#@login_check
def task_list_view():
    '''
        任务列表展示
    '''
    if request.method == 'GET':
        return render_template('task-list.html')

    try:
        draw = int(request.form.get('draw'))
        start = int(request.form.get('start'))
        length = int(request.form.get('length'))
        search_key = request.form.get('search[value]')
        order_column = request.form.get('order[0][column]') 
        order_column = request.form.get('order[0][dir]')
        data = [k for k in json.loads(requests.get('http://127.0.0.1:5555/api/tasks').text).values()]
        count = len(data)
        json_data = {
            'draw': draw,
            'recordsTotal': count,
            'recordsFiltered': count,
            'data': data
        }

    except Exception as e:
        print(e)

    return render_template_string(json.dumps(json_data))