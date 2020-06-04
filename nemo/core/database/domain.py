#!/usr/bin/env python3
# coding:utf-8
from . import daobase

class Domain(daobase.DAOBase):
    def __init__(self):
        super().__init__()
        self.table_name = 'domain'
        self.order_by = 'domain'


    def save_and_update(self, data):
        '''保存数据
        新增或更新一条数据
        返回值：id
        '''
        # 查询obj是否已存在
        obj = self.gets({'domain': data['domain']})
        # 如果已存在，则更新记录
        if obj and len(obj) > 0:
            data_update = {}
            self.copy_exist(data_update, data, 'org_id')

            return obj[0]['id'] if self.update(obj[0]['id'], data_update) else 0
        # 如果不存在，则生成新记录
        else:
            data_new = {'domain': data['domain']}
            self.copy_key(data_new, data, 'org_id')

            return self.add(data_new)
