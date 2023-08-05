# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 14:32:40
@LastEditTime: 2020-11-19 09:27:15
@LastEditors: HuangJingCan
@Description: 枚举类
"""

from enum import Enum, unique


class TagType(Enum):
    """
    @description: 标签类型
    """
    无 = 0
    限定 = 1
    稀有 = 2
    绝版 = 3
    隐藏 = 4


class SourceType(Enum):
    """
    @description: 用户次数配置来源类型
    """
    购买 = 1
    任务 = 2
    手动配置 = 3


class OperationType(Enum):
    """
    @description: 用户操作日志类型
    """
    add = 1
    update = 2
    delete = 3


class TaskType(Enum):
    """
    docstring：任务类型
    """
    掌柜有礼 = 1
    每日签到 = 2
    邀请新用户 = 3
    关注店铺 = 4
    加入店铺会员 = 5
    下单购买指定商品 = 6
    收藏商品 = 7
    浏览商品 = 8
    加入群聊 = 9
    分享群聊 = 10
    直播 = 11
    每周签到 = 12
    下单任意消费 = 13
    累计消费 = 14
    单笔订单消费 = 15
    新人有礼 = 16
    店长好礼 = 17
