#!/usr/bin/env python3
# coding:utf-8
import time
from nemo.core.tasks.taskapi import TaskAPI

taskapi = TaskAPI()


def t1():
    result = taskapi.start_task("add", args=[1, 2])
    print(result)
    return result['result']['task-id']


def t11():
    result = taskapi.start_task("nmap", kwargs={'task_name': 'nmap scan', 'options': {
                                'target': ('192.168.110.0/24','218.19.148.193'), 'port': '--top 1000','ping':False,'tech':'-sS'}})
    print(result)
    
    return result['result']['task-id']


def t2(task_id):
    result = taskapi.get_task_info(task_id)
    print(result)
    result = taskapi.get_task_result(task_id)
    print()
    print(result)


def t3():
    result = taskapi.get_tasks()  # state='STARTED')
    print(result)
    print(len(result['result']))


def t4(task_id):
    result = taskapi.revoke_task(task_id)
    print(result)

def t5():
    result = taskapi.start_task('iplocation',kwargs={'task_name':'get ip location','options':{'target':('218.19.148.193',)}})
    print(result)


def t7():
    result = taskapi.start_task('webtitle',kwargs={'task_name':'get web title','options':{'target':
        [{'ip':'218.19.148.193','port':[80,443]}]}})
    print(result)

def t8():
    result = taskapi.start_task('domainip',kwargs={'task_name':'get domain ip','options':{'target':
        ('www.sgcc.com.cn','www.csg.cn')}})
    print(result)

def t9():
    result = taskapi.start_task("portscan", kwargs={'task_name': 'portscan', 'options': {
                                'target': ('218.19.148.193',), 'port': '80,443,8080','org_id':9,'webtitle':True,'iplocation':True}})
    
    print(result)

#task_id = t11()
# t2(task_id)
# t3()
# time.sleep(1)
# t4(task_id)
#t5()
#t7()
#t8()
t9()
