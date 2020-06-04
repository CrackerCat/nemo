#!/usr/bin/env python3
# coding:utf-8

def test_org():
    from nemo.core.database.organization import Organization
    org = Organization()
    #row_id = org.add(data={'org_name':'hnsgcc','status':'enable','sort_order':200})
    #print(row_id)
    obj = org.get(9)
    print(obj)
    #data={'org_name':'cqsgcc2','status':'disable','sort_order':300}
    #print(org.update(8,data))
    #print(org.get(8))
    #print(org.delete(6))
    #print(org.gets(query={'org_name':'cqsgcc'},page=1,rows_per_page=2))
    #print(org.count())
    print(org.gets())

def test_ip():
    from nemo.core.database.ip import Ip
    from nemo.core.database.port import Port
    ip = Ip()
    port = Port()
    # row_id = ip.add(data={'ip':'192.168.3.1','org_id':None,'location':'上海','status':'enable'})
    # print(row_id)
    # obj = ip.get(row_id)
    # print(obj)
    # data={'ip':'192.168.3.10','org_id':3,'location':'上海2','status':'enable'}
    # print(ip.update(1,data))
    # print(ip.get(1))
    #print(org.delete(6))
    #print(ip.gets(query={'ip':'192.168.3.10'},page=1,rows_per_page=2))
    #print(ip.count())
    print(ip.gets_by_range(ip_start='192.168.1.1',ip_end='192.168.3.20'))

def test_port():
    from nemo.core.database.port import Port
    port = Port()
    #row_id = port.add(data={'ip_id':3,'port':80,'status':'open'})
    #print(row_id)
    # obj = port.get(row_id)
    # print(obj)
    #print(port.get(2))
    print(port.gets(query={'ip_id':58}))

def test_port_attr():
    from nemo.core.database.attr import PortAttr
    pa = PortAttr()
    # row_id = pa.add(data={'r_id':2,'source':'scan','tag':'service','content':'nginx'})
    # print(row_id)
    # obj = pa.get(row_id)
    # print(obj)
    print(pa.get(1))
    print(pa.gets(query={'r_id':2}))
    print(pa.gets(query={'r_id':2},fields=('tag','content')))

def test1():
    from nemo.core.database.ip import Ip
    ip = Ip()
    data = ip.gets(query={'ip':'192.168.3.10'})
    print(data)

if __name__ == '__main__':
    #main()
    test_org()
    #test_ip()
    #test_port()
    #test_port_attr()
    #test1()
   
