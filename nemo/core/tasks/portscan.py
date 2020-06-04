#!/usr/bin/env python3
# coding:utf-8
from .taskbase import TaskBase
from .nmap import Nmap
from .ipdomain import IpDomain
from .webtitle import WebTitle


class PortScan(TaskBase):
    '''端口扫描综合任务
    参数：options
        {   
            'target':   [ip1,ip2,ip3...],ip列表（nmap格式）
            'port':     '1-65535'或者'--top-ports 1000',nmap能识别的端口格式
            'org_id':   id,target关联的组织机构ID
            'rate':     1000,扫描速率
            'ping':     True/False，是否PING
            'tech':     '-sT'/'-sS'/'-sV'，扫描技术
            'webtitle': True/False，是否读取网站IP地址
            'iplocation':   True/False，是否获取IP归属地
        }
    '''

    def __init__(self):
        super().__init__()
        # 任务名称
        self.task_name = 'portscan'
        # 任务描述
        self.task_description = '端口扫描综合任务'
        # 默认参数：
        self.source = 'portscan'
        self.result_attr_keys = ('service', 'banner', 'title')
        self.webtitle = False
        self.iplocation = False

    def prepare(self, options):
        '''解析参数
        '''
        self.org_id = None if 'org_id' not in options else options['org_id']
        self.webtitle = False if 'webtitle' not in options else options['webtitle']
        self.iplocation = False if 'iplocation' not in options else options['iplocation']

    def run(self, options):
        '''执行端口扫描任务
        '''
        self.prepare(options)       
        # nmap扫描
        nmap_app = Nmap()
        nmap_app.prepare(options)
        ip_ports = nmap_app.execute()
        # IP归属地
        if self.iplocation == True:
            ipdomain_app = IpDomain()
            ipdomain_app.execute_iplocation(ip_ports)
        # 端口的title
        if self.webtitle == True:
            webtitle_app = WebTitle()
            webtitle_app.execute(ip_ports)
        # 保存数据
        result = self.save_ip(ip_ports)
        result['status'] = 'success'

        return result
