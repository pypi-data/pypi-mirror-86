import pytz
from datetime import datetime
from pymodm import fields, MongoModel
from enum import IntEnum
from ..connection.connect import *


class HolderType(IntEnum):
    AIMS = 0


class HolderLevel(IntEnum):
    SUPER = 99
    A = 0

    @staticmethod
    def level_from(text):
        if text.lower() == 'super':
            return HolderLevel.SUPER
        else:
            return HolderLevel.A


class HolderStatus(IntEnum):
    NORMAL = 0
    INVALID = -1


class Holder(MongoModel):
    """持仓人信息"""
    id = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    balance = fields.FloatField()
    create_date = fields.DateTimeField()
    update_date = fields.DateTimeField()
    level = fields.IntegerField()
    status = fields.IntegerField(default=0)

    def print_desc(self):
        print("{}:\t{}\t{}\t{}".format(self.id, self.name, self.balance, self.update_date))

    class Meta:
        collection_name = CN_FIN_HOLDER
        connection_alias = DB_FINANCIAL


class Event(MongoModel):
    """事件信息"""
    id = fields.IntegerField(primary_key=True)
    content = fields.CharField()
    note = fields.CharField()
    date = fields.DateTimeField()

    class Meta:
        collection_name = CN_FIN_EVENT
        connection_alias = DB_FINANCIAL


class Record(MongoModel):
    """持仓人相关操作记录"""
    holder = fields.IntegerField()
    event = fields.IntegerField()
    balance_before = fields.FloatField()
    balance_after = fields.FloatField()
    date = fields.DateTimeField()

    class Meta:
        collection_name = CN_FIN_RECORD
        connection_alias = DB_FINANCIAL
