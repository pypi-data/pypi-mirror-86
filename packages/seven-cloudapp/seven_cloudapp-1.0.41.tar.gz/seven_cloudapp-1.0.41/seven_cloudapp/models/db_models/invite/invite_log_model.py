
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class InviteLogModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None):
        super(InviteLogModel, self).__init__(InviteLog, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class InviteLog:

    def __init__(self):
        super(InviteLog, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.open_id = ""  # 邀请人OpenID
        self.invite_open_id = ""  # 受邀人OpenID
        self.is_handle = 0  # 是否处理（1处理0未处理）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_day = 0  # 创建天(20201111)

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'open_id', 'invite_open_id', 'is_handle', 'create_date', 'create_day']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "invite_log_tb"
    