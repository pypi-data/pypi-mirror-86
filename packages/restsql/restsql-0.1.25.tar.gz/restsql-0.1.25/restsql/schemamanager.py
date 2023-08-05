# -*- coding: UTF-8 -*-
import threading
from threading import Timer

from restsqldb import EnumDataBase
from model import Table, StringField, IntField, BoolField, NumberField


def _delete_by_name(tables, table_name):
    for table in tables:
        if table.table_name == table_name:
            tables.remove(table)
            return None


class SchemaManager:
    """
    db_settings外包装：管理db_settings
    对外提供active_daemon()函数以启动db_settings定时管理。
    目前只支持impala
    """

    def __init__(self, db_settings, period, table_map=None):
        """
        初始化
        :param period: 刷新间隔时间
        """
        self._period = period
        self._db_settings = db_settings  # 绑定系统中的单例db_settings
        self._daemon_thread = None
        self.table_map = table_map

    def active_daemon(self):
        """
        启动守护进程。请在配置好db_settings后再启动。
        :return: None
        """
        try:
            self._daemon_thread = threading.Thread(target=self._query_schema, args=(self._period,),
                                                   name="SchemaManager")
            self._daemon_thread.setDaemon(True)  # 注意以守护进程的形式开启manager
            self._daemon_thread.start()
        except:
            raise Exception("Can't start thread")

    def _query_schema(self, period):
        """
        每隔period时间执行一次本函数。
        遍历每个db_setting:
            若是IMPALA:
                1. 锁定
                2. 发送请求获取所有table
                3. 对所有不在black_tables里、tables里的表发送查询schema请求
                4. 解析结果，并根据black_fields更新schema
            若是其他:
                忽视
        :param period: 更新间隔时间
        :return: None
        """
        for name in self._db_settings:
            if self._db_settings[name].db_type == EnumDataBase.IMPALA:
                db_setting = self._db_settings[name]
                # db_setting.lock.acquire()  # 1. 锁定
                table_list = db_setting.impala_client.run_sql("show tables")  # 2. 发送请求获取所有table
                for table_dict in table_list:  # 对每个table
                    table_name = table_dict.values()[0]
                    if table_name not in db_setting.black_tables:  # 3. 对所有不在black_tables里、tables里的表发送查询schema请求
                        field_list = db_setting.impala_client.run_sql("describe {}".format(table_name))
                        black_fields = None
                        if table_name in db_setting.black_fields:
                            black_fields = db_setting.black_fields[table_name]
                        fields = {}
                        _delete_by_name(db_setting.tables, table_name)  # 删除原来的类
                        for field_dict in field_list:  # 4. 解析结果，并根据black_fields更新schema
                            if black_fields is None or field_dict['name'] not in black_fields:
                                if field_dict['type'] == 'int' or field_dict['type'] == 'tinyint' or \
                                        field_dict['type'] == 'timestamp':
                                    fields[field_dict['name']] = IntField()
                                elif field_dict['type'] == 'bigint' or field_dict['type'] == 'double':
                                    fields[field_dict['name']] = NumberField()
                                elif field_dict['type'] == 'string':
                                    fields[field_dict['name']] = StringField()
                                elif field_dict['type'] == 'bool':
                                    fields[field_dict['name']] = BoolField()
                        table = type(table_name, (Table,), {'table_name': table_name, 'fields': fields})
                        db_setting.tables.append(table)
                        if self.table_map is not None:
                            self.table_map[table_name] = "{}.{}".format(db_setting.name, table_name)
                # db_setting.lock.release()  # 释放锁
        Timer(period, self._query_schema).start()
