#!/usr/bin/env python3
# coding:utf-8

from celery import Celery, Task
from .nmap import Nmap
from .ipdomain import IpDomain
from .webtitle import WebTitle
from .portscan import PortScan

celery_app = Celery('nemo', broker='amqp://', backend='rpc://')


class UpdateTaskStatus(Task):
    '''在celery的任务异步完成时，显示完成状态和结果
    '''
    def on_success(self, retval, task_id, args, kwargs):
        print('task {} done: {}'.format(task_id, retval))
        return super(UpdateTaskStatus, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task {} fail, reason: {}'.format(task_id, exc))
        return super(UpdateTaskStatus, self).on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(base=UpdateTaskStatus)
def add(x, y):
    '''test
    '''
    import time
    import random
    r = random.randint(1, 30)
    time.sleep(r)


@celery_app.task(base=UpdateTaskStatus)
def nmap(task_name, options):
    '''调用nmap进行端口扫描
    '''
    task_app = Nmap()
    result = task_app.run(options)
    return result


@celery_app.task(base=UpdateTaskStatus)
def iplocation(task_name, options):
    '''获取ip的归属地
    '''
    task_app = IpDomain()
    result = task_app.run_iplocation(options)
    return result

@celery_app.task(base=UpdateTaskStatus)
def webtitle(task_name, options):
    '''获取title
    '''
    task_app = WebTitle()
    result = task_app.run(options)
    return result

@celery_app.task(base=UpdateTaskStatus)
def domainip(task_name, options):
    '''查询域名IP
    '''
    task_app = IpDomain()
    result = task_app.run_domainip(options)
    return result

@celery_app.task(base=UpdateTaskStatus)
def portscan(task_name, options):
    '''端口扫描综合任务
    '''
    task_app = PortScan()
    result = task_app.run(options)
    return result

