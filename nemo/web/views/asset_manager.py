#!/usr/bin/env python3
#coding:utf-8

import re
import IPy
import json
import hashlib
import socket
import requests
from urllib.parse import urlparse

from flask import Flask, render_template, Blueprint, url_for, redirect, request, render_template_string,jsonify
from .authenticate import login_check
from core.database.ip import Ip
from core.database.organization import Organization
from core.database.domain import Domain
from core.database.port import Port

asset_manager = Blueprint('asset_manager', __name__)


class AssetListParser(object):
    '''
    资产列表数据解析
        因为资产列表采用混合模式输入，可以输入域名、IP地址和网段，因此需要根据不同的输入做解析。
        1. 列表中输入域名时
        2. 输入的是IP时，如果不是私有地址时反查IP对应的域名，返回当前使用的域名，生成C段地址给扫描器；
        3. 输入网段时，由网段生成IP地址生成器返回给扫描器。
        4. 获取地理位置
    '''
    def __init__(self, asset_form_data):
        self.ip_table = Ip()
        self.org_table = Organization()
        self.domain_table = Domain()
        self.get_form_data(asset_form_data)
        self.req_form_parser()


    def get_form_data(self, data):
        self.asset_list = data.get('asset_list')
        self.asset_type = data.get('asset_type')
        #self.status = asset_form_data.get('status')
        self.org_name = data.get('org_name').encode('utf-8')

    def req_form_parser(self):
        '''
            表单参数处理
        '''
        try:
            for asset in self.asset_list:
                '''
                    资产类型是IP地址或网段处理并存入IP表
                '''
                if self.asset_type == 'ip':
                    if re.findall('^(?:\d{1,3}\.){3}\d{1,3}$', asset):
                        ip = re.findall('^(?:\d{1,3}\.){3}\d{1,3}$', asset)[0]
                    elif re.findall('^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$', asset):
                        ip = re.findall('^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$', asset)[0]
                    self.ip_table.add(data = {'ip': ip, 'org_id': self.get_org_id(),'status': 'alive'})
                elif self.asset_type == 'domain':
                    '''
                        资产为domain时，检查输入并将其存入domain表
                    '''
                    domain = urlparse(asset).netloc if urlparse(asset).netloc else urlparse(asset).path.split('/')[0]
                    print(self.domain_table.add(data = {'domain': domain.strip(),'org_id': self.get_org_id()}))
        except Exception as e:
            print(e)


    def get_org_id(self):
        '''
            查询机构ID
            如果机构表没有该机构，则将其插入表中并返回org_id
            :return: org_id
        '''
        row = self.org_table.gets(query = {'org_name': self.org_name}, page = 1, rows_per_page = 1)
        return row[0]['id'] if row else self.org_table.add(data = {'org_name' : self.org_name, 'status':'enable'})


@asset_manager.route('/asset-add', methods = ['GET', 'POST'])
#@login_check
def asset_add_view():
    '''
        添加资产
        1. 添加IP或域名地址
        2. 增加通过excel模板导入
    '''
    if request.method == 'POST':
        asset_form_data = {
            'org_name': request.form['org_name'],
            'asset_list': request.form['asset_list'].split('\n'),
            'asset_type': 'domain' if request.form['asset_type'] == '1' else 'ip'
        }
        AssetListParser(asset_form_data)

    return render_template('asset-add.html')

@asset_manager.route('/ip-list', methods = ['GET', 'POST'])
#@login_check
def ip_asset_view():
    '''
        IP资产列表展示
    '''
    if request.method == 'GET':
        return render_template('ip-list.html')
    
    ip_table = Ip()
    port_table = Port()
    org_table = Organization()
    ip_list = []
    json_data = {}
    index = 1
    
    org_name = request.form.get('org_name')
    ip_addr = request.form.get('ip_address')
    port = request.form.get('port')
    if(org_name or ip_addr or port):
        pass
    try:
        draw = int(request.form.get('draw'))
        start = int(request.form.get('start'))
        length = int(request.form.get('length'))
        search_key = request.form.get('search[value]')
        order_column = request.form.get('order[0][column]')  # 排序字段索引
        order_column = request.form.get('order[0][dir]')  #排序規則：ase/desc
        for ip_row in ip_table.gets(page = (start//length) + 1, rows_per_page = length):
            ip_list.append({
                'id':ip_row['id'],        #表内序号
                "index":index+start,              #显示序号
                "org_name":org_table.get(int(ip_row['org_id']))['org_name'] if ip_row['org_id'] else '',
                "ip":ip_row['ip'],
                "status":ip_row['status'],
                "location":ip_row['location'],
                "port":'\n'.join(['{}:{}'.format(row['port'], row['status']) for row in port_table.gets(query = {'ip_id': ip_row['id']})]),
                "create_time":str(ip_row['create_datetime']),
                "update_time":str(ip_row['update_datetime'])
            })
            index += 1

        count = ip_table.count()
        json_data = {
            'draw': draw,
            'recordsTotal': count,
            'recordsFiltered': count,
            'data': ip_list
        }

    except Exception as e:
        print(e)

    return render_template_string(json.dumps(json_data))

@asset_manager.route('/domain-list', methods = ['GET', 'POST'])
#@login_check
def domain_asset_view():
    '''
        页面上显示域名资产，datatable前端ajax请求进行分页
    '''
    if request.method == 'GET':
        return render_template('domain-list.html')
    domain_list = []
    json_data = {}
    ip_table = Ip()
    org_table = Organization()
    domain_table = Domain()
    index = 1

    draw = int(request.form.get('draw'))
    start = int(request.form.get('start'))
    length = int(request.form.get('length'))
    search_key = request.form.get('search[value]')
    order_column = request.form.get('order[0][column]')  # 排序字段索引
    order_column = request.form.get('order[0][dir]')  #排序規則：ase/desc

    count = domain_table.count()
    try:
        for domain_row in domain_table.gets(page = start/length + 1, rows_per_page = length):
            domain_list.append({
                'id':domain_row['id'], 
                "index":index+start,
                "domain": domain_row['domain'],
                "ip":'\n'.join([ip_row['ip'] for ip_row in ip_table.gets(query={'org_id': domain_row['org_id']})]),
                "title": 'Title_test',
                "org_name":org_table.get(int(domain_row['org_id']))['org_name'] if domain_row['org_id'] else '',
                "create_time":str(domain_row['create_datetime']),
                "update_time":str(domain_row['update_datetime'])
            })
            index += 1
        json_data = {
                'draw': draw,
                'recordsTotal': count,
                'recordsFiltered': count,
                'data': domain_list
            }
    except Exception as e:
        print(e)
    return render_template_string(json.dumps(json_data))