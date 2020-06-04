#!/usr/bin/env python3
# coding:utf-8
from . import dbutils
from . import daobase


class Ip(daobase.DAOBase):
    def __init__(self):
        super().__init__()
        self.table_name = 'ip'
        self.order_by = 'ip_int'

    def ip2int(self, ip):
        '''将点分的字符串IP转换为整数值
        '''
        ips = ip.strip().split('.')
        x = int(ips[0]) << 24 | int(ips[1]) << 16 | int(
            ips[2]) << 8 | int(ips[3])
        return x

    def add(self, data):
        '''增加一条IP记录：计算IP的整数值
        '''
        data['ip_int'] = self.ip2int(data['ip'])
        return super().add(data)

    def update(self, Id, data):
        '''更新一条IP记录：如果IP地址需要更新，重新计算整数值
        '''
        if 'ip' in data:
            data['ip_int'] = self.ip2int(data['ip'])
        return super().update(Id, data)

    def gets_by_range(self, ip_start, ip_end, query=None, fields=None, page=1, rows_per_page=None, order_by=None):
        '''根据IP范围查询IP
        ip_start:   起始ip值
        ip_end:     结束ip值
        query:      查询条件，字典格式如{'name':'hello','port':80}，多个条件默认是and
        fields:     要返回的字段，列表格式('id','name','port')
        page:       分页位置，从1开始
        rows_per_page:  每页的记录数
        order_by     :  排序字段
        '''
        sql = []
        param = []
        sql.append('select {} from {} '.format(
            self.fill_fields(fields), self.table_name))
        # IP范围
        sql.append('where ip_int between %s and %s ')
        if type(ip_start) == str:
            param.append(self.ip2int(ip_start))
            param.append(self.ip2int(ip_end))
        else:
            param.append(ip_start)
            param.append(ip_end)
        # 查询条件
        if query and len(query) > 0:
            sql.append(self.fill_where(query, param, pre_word='and'))
        # 排序、分页
        sql.append(self.fill_order_by_and_limit(
            param, order_by, page, rows_per_page))

        return dbutils.queryall(''.join(sql), param)

    def save_and_update(self, data):
        '''保存数据
        新增或更新一条数据
        返回值：id
        '''
        # 查询obj是否已存在
        obj = self.gets({'ip': data['ip']})
        # 如果已存在，则更新记录
        if obj and len(obj) > 0:
            data_update = {}
            self.copy_exist(data_update, data, 'status')
            self.copy_exist(data_update, data, 'org_id')
            self.copy_exist(data_update, data, 'location')

            return obj[0]['id'] if self.update(obj[0]['id'], data_update) else 0
        # 如果不存在，则生成新记录
        else:
            data_new = {'ip': data['ip']}
            self.copy_key(data_new, data, 'status','alive')
            self.copy_key(data_new, data, 'org_id')
            self.copy_key(data_new, data, 'location')

            return self.add(data_new)
