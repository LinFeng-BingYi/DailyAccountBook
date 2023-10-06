#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Linfeng_Bingyi
# @Contact : linfengbingyi@qq.com
# @File    : ConstArgs.py
# @Time    : 2023/9/10 15:10
# @Dsc     : 定义所有公共常量

# 基本需求
NECESSITY = {'True': '基本', 'False': '过度', 'Unknown': '一般'}


# 支出相关的常量
class ExpenseConst:
    # 类别
    CATEGORY = {
        0: "饮食",
        1: "出行",
        2: "住房",
        3: "服饰",
        4: "日用品",
        5: "家居",
        6: "医疗",
        7: "固定消费",
        8: "办公",
        9: "学习教育",
        10: "休闲娱乐",
        11: "往来",
        12: "金融理财",
        13: "动植物",
        14: "非本人相关",
        15: "慈善捐赠",
        16: "借贷",
        17: "杂项支出"
    }
    # 显示记录的表格表头
    TABLEWIDGET_COLUMN_HEAD = {'基本需求': 'necessity', '数值': 'value', '类别': 'category', '细则': 'detail',
                               '描述': 'describe', '支出账户': 'from', '关联账户': 'associatedFund', '操作': ''}


# 收入相关的常量
class IncomeConst:
    CATEGORY = {
        0: "职业收入",
        1: "储蓄利息",
        2: "投资理财",
        3: "往来",
        4: "杂项收入",
        5: "非本人相关",
        6: "慈善捐赠",
        7: "借贷",
    }
    TABLEWIDGET_COLUMN_HEAD = {'数值': 'value', '类别': 'category', '细则': 'detail', '描述': 'describe',
                               '收入账户': 'to', '关联账户': 'associatedFund', '操作': ''}


class MovementConst:
    TABLEWIDGET_COLUMN_HEAD = {'数值': 'value', '细则': 'detail', '描述': 'describe',
                               '转出账户': 'from', '转入账户': 'to', '操作': ''}


# 存款账户相关的常量
class FundConst:
    CATEGORY = {
        None: "无",
        0: "微信零钱",
        1: "中国银行卡",
        2: "羊城通",
        3: "支付宝余额宝",
        4: "代管存款"
    }
    TABLEWIDGET_COLUMN_HEAD = {}


expenseConst = ExpenseConst()
incomeConst = IncomeConst()
movementConst = MovementConst()
fundConst = FundConst()
