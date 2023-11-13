#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Linfeng_Bingyi
# @Contact : linfengbingyi@qq.com
# @File    : AccountBookXML.py
# @Time    : 2023/9/9 16:40
from xml.etree import ElementTree as et
import os
from decimal import Decimal
from collections import OrderedDict
import pandas as pd


def pretty_xml(element, indent='    ', newline='\n', level=0):  # element为传进来的Element类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for sub_element in temp:
        if temp.index(sub_element) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            sub_element.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            sub_element.tail = newline + indent * level
        pretty_xml(sub_element, indent, newline, level=level + 1)  # 对子元素进行递归操作


class AccountBookXMLProcessor:

    def __init__(self, file_path):
        if os.path.exists(file_path):
            # print(file_path)
            self.xml_tree = et.parse(file_path)
            self.e_dailyAccountBook = self.xml_tree.getroot()
        else:
            self.e_dailyAccountBook = et.Element("DailyAccountBook")
            self.xml_tree = et.ElementTree(self.e_dailyAccountBook)

    def getSpecificDateElement(self, date_str):
        """
        Describe: 根据日期字符串获取指定的day元素

        Args:
            date_str: str
                格式为"yyyyMMdd"

        Returns:
            若找到指定日期的元素，则返回Element类型的day元素.

            若未找到指定year，则返回int类型的0；若未找到指定month，则返回int类型的1；若未找到指定day，则返回int类型的2。
            int型返回值用于控制从何处开始初始化日期元素。
        """
        if date_str is None:
            raise ValueError("date_str不能为空!")
        if len(date_str) != 8 or not date_str.isdigit():
            print("日期格式不正确！")
            raise ValueError('日期格式不正确！必须为"yyyyMMdd"格式')

        e_year = self.e_dailyAccountBook.find(".//year[@value='{}']".format(date_str[:4]))
        if e_year is None:
            return 0
        e_month = e_year.find(".//month[@value='{}']".format(date_str[4:6]))
        if e_month is None:
            return 1
        e_day = e_month.find(".//day[@value='{}']".format(date_str[6:]))
        if e_day is None:
            return 2
        return e_day

    def parseBalance(self):
        e_balance = self.e_dailyAccountBook.find(".//balance")
        balance_list = []
        for e_fund in list(e_balance):
            # balance_dict = {"value": float(e_fund.find('.//value').text),
            #                 "category": int(e_fund.find('.//category').text),
            #                 "fundName": e_fund.find('.//fundName').text}
            balance_dict = OrderedDict([("value", float(e_fund.find('.//value').text)),
                                        ("category", int(e_fund.find('.//category').text)),
                                        ("fundName", e_fund.find('.//fundName').text),
                                        ("ignore", True if e_fund.find('.//ignore').text.lower() == 'true' else False)])
            balance_list.append(balance_dict)
        return balance_list

    def parseSpecificDateElement(self, date_str):
        """
        Describe: 根据日期字符串获取指定的day元素，然后解析该day元素下的所有子元素

        Args:
            date_str: str
                格式为"yyyyMMdd"

        Returns: dict[str, list[dict]]
            若找到指定日期的元素，则返回dict类型的数据
            若未找到指定日期，则返回None
            注意：假设某天没有支出/收入/转移操作，那么返回结果dict中便不存在'expenses'/'incomes'/'movements'键

            example:
                return_dict = {
                    'expenses': [
                        {'necessity': 'True', 'value': Decimal('100.00'), 'category': 1, 'detail': 'expense detail', 'describe': 'An expense record', 'from': 0, 'associatedFund': 'None'},
                        ...
                    ],
                    'incomes': [
                        {'value': Decimal('300.00'), 'category': 3, 'detail': 'income detail', 'describe': 'An income record', 'to': 1, 'associatedFund': 'None'},
                        ...
                    ],
                    'movements': [
                        {'value': Decimal('500.00'), 'detail': 'movement detail', 'describe': 'An movement record', 'from': 0, 'to': 1},
                        ...
                    ],
                    'variation': [
                        {'category': 0, 'out': Decimal('100.00'), 'in': Decimal('300.00')},
                        ...
                    ]
                }
        """
        e_date = self.getSpecificDateElement(date_str)

        if isinstance(e_date, int):
            print("未找到这一天的数据！")
            return None

        parse_dict = dict()

        for child_node in list(e_date):
            if child_node.tag == 'expenses':
                e_expenses = e_date.find(".//expenses")
                expenses_list = [self.parseExpense(e_expense) for e_expense in list(e_expenses)]
                parse_dict['expenses'] = expenses_list
            elif child_node.tag == 'incomes':
                e_incomes = e_date.find(".//incomes")
                incomes_list = [self.parseIncome(e_income) for e_income in list(e_incomes)]
                parse_dict['incomes'] = incomes_list
            elif child_node.tag == 'movements':
                e_movements = e_date.find(".//movements")
                movements_list = [self.parseMovement(e_movement) for e_movement in list(e_movements)]
                parse_dict['movements'] = movements_list
            elif child_node.tag == 'variation':
                e_variation = e_date.find(".//variation")
                variation_list = [self.parseVariation(e_fund) for e_fund in list(e_variation)]
                parse_dict['variation'] = variation_list
            else:
                print("解析day元素时，出现未知类型的节点名:", child_node.tag)

        return parse_dict

    def parseExpense(self, e_expense):
        # expense_dict = {
        #     'necessity': True if (e_expense.attrib['necessity'].lower() == 'true') else False,
        #     'value': float(e_expense.find('.//value').text),
        #     'category': int(e_expense.find('.//category').text),
        #     'detail': e_expense.find('.//detail').text,
        #     'describe': e_expense.find('.//describe').text,
        #     'from': int(e_expense.find('.//from').text),
        #     'associatedFund': int(e_expense.attrib['associatedFund']) if (
        #             ('associatedFund' in e_expense.attrib) and e_expense.attrib['associatedFund'] != 'None') else None
        # }
        expense_dict = OrderedDict([
            ('necessity', e_expense.attrib['necessity']),
            ('value', Decimal(e_expense.find('.//value').text).quantize(Decimal('0.00'))),
            ('category', int(e_expense.find('.//category').text)),
            ('detail', e_expense.find('.//detail').text),
            ('describe', e_expense.find('.//describe').text),
            ('from', int(e_expense.find('.//from').text)),
            ('associatedFund', int(e_expense.attrib['associatedFund']) if (
                    ('associatedFund' in e_expense.attrib) and e_expense.attrib['associatedFund'] != 'None') else None)
        ])
        # print(expense_dict['value'])

        return expense_dict

    def parseIncome(self, e_income):
        # income_dict = {
        #     'associatedFund': int(e_income.attrib['associatedFund']) if (
        #             ('associatedFund' in e_income.attrib) and e_income.attrib['associatedFund'] != 'None') else None,
        #     'value': float(e_income.find('.//value').text),
        #     'category': int(e_income.find('.//category').text),
        #     'detail': e_income.find('.//detail').text,
        #     'describe': e_income.find('.//describe').text,
        #     'to': int(e_income.find('.//to').text)
        # }
        income_dict = OrderedDict([
            ('value', Decimal(e_income.find('.//value').text).quantize(Decimal('0.00'))),
            ('category', int(e_income.find('.//category').text)),
            ('detail', e_income.find('.//detail').text),
            ('describe', e_income.find('.//describe').text),
            ('to', int(e_income.find('.//to').text)),
            ('associatedFund', int(e_income.attrib['associatedFund']) if (
                    ('associatedFund' in e_income.attrib) and e_income.attrib['associatedFund'] != 'None') else None)
        ])

        return income_dict

    def parseMovement(self, e_movement):
        # movement_dict = {
        #     'value': float(e_movement.find('.//value').text),
        #     'detail': e_movement.find('.//detail').text,
        #     'describe': e_movement.find('.//describe').text,
        #     'from': int(e_movement.find('.//from').text),
        #     'to': int(e_movement.find('.//to').text)
        # }
        movement_dict = OrderedDict([
            ('value', Decimal(e_movement.find('.//value').text).quantize(Decimal('0.00'))),
            ('detail', e_movement.find('.//detail').text),
            ('describe', e_movement.find('.//describe').text),
            ('from', int(e_movement.find('.//from').text)),
            ('to', int(e_movement.find('.//to').text))
        ])

        return movement_dict

    def parseVariation(self, e_fund):
        # fund_dict = {
        #     'category': int(e_fund.find('.//category').text),
        #     'out': float(e_fund.find('.//out').text),
        #     'in': float(e_fund.find('.//in').text),
        # }
        fund_dict = OrderedDict([
            ('category', int(e_fund.find('.//category').text)),
            ('out', Decimal(e_fund.find('.//out').text).quantize(Decimal('0.00'))),
            ('in', Decimal(e_fund.find('.//in').text).quantize(Decimal('0.00'))),
        ])

        return fund_dict

    def createChildElement(self, e_parent, child_name, child_text, chile_attr=None):
        if chile_attr is None:
            chile_attr = {}
        e_child = et.SubElement(e_parent, child_name, attrib=chile_attr)
        e_child.text = child_text
        return e_child

    def switch_caseInitStartDate(self, init_start, date_str):
        # 模拟C++中switch-case控制语句，不使用break的情况
        if init_start == 0:
            self.createChildElement(self.e_dailyAccountBook, 'year', None, {'value': date_str[:4]})
            init_start += 1
        if init_start == 1:
            e_year = self.e_dailyAccountBook.find(".//year[@value='{}']".format(date_str[:4]))
            self.createChildElement(e_year, 'month', None, {'value': date_str[4:6]})
        #     init_start += 1
        # if init_start == 2:
        e_year = self.e_dailyAccountBook.find(".//year[@value='{}']".format(date_str[:4]))
        e_month = e_year.find(".//month[@value='{}']".format(date_str[4:6]))
        e_date = self.createChildElement(e_month, 'day', None, {'value': date_str[6:]})
        return e_date

    def organizeExpense(self, expense_dict: dict, date_str):
        e_date = self.getSpecificDateElement(date_str)

        if isinstance(e_date, int):
            print("未找到这一天的数据！")

            e_date = self.switch_caseInitStartDate(e_date, date_str)

        e_expenses = e_date.find(".//expenses") if e_date.find(".//expenses") is not None else self.createChildElement(e_date, 'expenses', None)
        e_expense = et.SubElement(e_expenses, 'expense')

        self.organizeVariation(expense_dict, e_date)

        for key, value in expense_dict.items():
            if key == 'necessity':
                e_expense.set('necessity', expense_dict['necessity'])
            elif key == 'associatedFund':
                e_expense.set('associatedFund', expense_dict['associatedFund'])
            else:
                self.createChildElement(e_expense, key, value)

        # print(et.tostring(e_expenses, 'utf8'))

    def organizeIncome(self, income_dict: dict, date_str):
        e_date = self.getSpecificDateElement(date_str)

        if isinstance(e_date, int):
            print("未找到这一天的数据！")

            e_date = self.switch_caseInitStartDate(e_date, date_str)

        e_incomes = e_date.find(".//incomes") if e_date.find(".//incomes") is not None else self.createChildElement(e_date, 'incomes', None)
        e_income = et.SubElement(e_incomes, 'income')

        self.organizeVariation(income_dict, e_date)

        for key, value in income_dict.items():
            if key == 'associatedFund':
                e_income.set('associatedFund', income_dict['associatedFund'])
            else:
                self.createChildElement(e_income, key, value)

    def organizeMovement(self, movement_dict: dict, date_str):
        e_date = self.getSpecificDateElement(date_str)

        if isinstance(e_date, int):
            print("未找到这一天的数据！")

            e_date = self.switch_caseInitStartDate(e_date, date_str)

        e_movements = e_date.find(".//movements") if e_date.find(".//movements") is not None else self.createChildElement(e_date, 'movements', None)
        e_movement = et.SubElement(e_movements, 'movement')
        for key, value in movement_dict.items():
            self.createChildElement(e_movement, key, value)

        self.modifyBalance(movement_dict['from'], Decimal(movement_dict['value'])*(-1))
        self.modifyBalance(movement_dict['to'], Decimal(movement_dict['value']))

    def modifyBalance(self, fund_category, increment_value: Decimal):
        """
        Describe:

        Args:
            fund_category: int or str
                存款账户类型
            increment_value: Decimal
                余额增量，为正或负
        """
        e_value = self.e_dailyAccountBook.find(".//balance").find(".//fund[category='{}']".format(fund_category)).find(".//value")
        e_value.text = str((Decimal(e_value.text) + increment_value).quantize(Decimal('0.00')))

    def organizeVariation(self, change_dict, e_date):
        e_variation = e_date.find(".//variation") if e_date.find(".//variation") is not None else self.createChildElement(e_date, 'variation', None)
        if 'from' in change_dict:
            if e_variation.find(".//fund[category='{}']".format(change_dict['from'])) is None:
                e_fund = self.createChildElement(e_variation, 'fund', None)
                self.createChildElement(e_fund, 'category', change_dict['from'])
                self.createChildElement(e_fund, 'out', '0.0')
                self.createChildElement(e_fund, 'in', '0.0')
            e_fund_variety = e_variation.find(".//fund[category='{}']/out".format(change_dict['from']))
            e_fund_variety.text = str((Decimal(e_fund_variety.text) + Decimal(change_dict['value'])).quantize(Decimal('0.00')))
            self.modifyBalance(change_dict['from'], Decimal(change_dict['value'])*(-1))

            self.organizeAssociatedFund(e_variation, change_dict, 'from')
        if 'to' in change_dict:
            if e_variation.find(".//fund[category='{}']".format(change_dict['to'])) is None:
                e_fund = self.createChildElement(e_variation, 'fund', None)
                self.createChildElement(e_fund, 'category', change_dict['to'])
                self.createChildElement(e_fund, 'out', '0.0')
                self.createChildElement(e_fund, 'in', '0.0')
            e_fund_variety = e_variation.find(".//fund[category='{}']/in".format(change_dict['to']))
            e_fund_variety.text = str((Decimal(e_fund_variety.text) + Decimal(change_dict['value'])).quantize(Decimal('0.00')))
            self.modifyBalance(change_dict['to'], Decimal(change_dict['value']))

            self.organizeAssociatedFund(e_variation, change_dict, 'to')

    def reversalVariation(self, change_dict, e_date):
        """
        Describe: 删除某条记录时，需要冲正原来的记录，将回退对应的存款账户数值变化、以及余额

        Args:
            change_dict: dict
                记录字典
            e_date: Element
                指定日期的day元素
        """
        e_variation = e_date.find(".//variation")
        if e_variation is None:
            print("冲正记录时异常！！该记录不存在余额变化")
            return
        if 'from' in change_dict:
            e_fund_variety = e_variation.find(".//fund[category='{}']/out".format(change_dict['from']))
            if e_fund_variety is None:
                print("冲正记录时异常！！该记录不存在余额变化")
                return
            e_fund_variety.text = str((Decimal(e_fund_variety.text) - Decimal(change_dict['value'])).quantize(Decimal('0.00')))
            self.modifyBalance(change_dict['from'], Decimal(change_dict['value']))

            self.reversalAssociatedFund(e_variation, change_dict, 'from')
        if 'to' in change_dict:
            e_fund_variety = e_variation.find(".//fund[category='{}']/in".format(change_dict['to']))
            if e_fund_variety is None:
                print("冲正记录时异常！！该记录不存在余额变化")
                return
            e_fund_variety.text = str((Decimal(e_fund_variety.text) - Decimal(change_dict['value'])).quantize(Decimal('0.00')))
            self.modifyBalance(change_dict['to'], Decimal(change_dict['value'])*(-1))

            self.reversalAssociatedFund(e_variation, change_dict, 'to')

    def organizeAssociatedFund(self, e_variation, change_dict, from_or_to):
        # print(change_dict['associatedFund'])
        if 'associatedFund' in change_dict and change_dict['associatedFund'] != 'None':
            print('执行了associatedFund，操作为', from_or_to)
            if e_variation.find(".//fund[category='{}']".format(change_dict['associatedFund'])) is None:
                e_associated_fund = self.createChildElement(e_variation, 'fund', None)
                self.createChildElement(e_associated_fund, 'category', change_dict['associatedFund'])
                self.createChildElement(e_associated_fund, 'out', '0.0')
                self.createChildElement(e_associated_fund, 'in', '0.0')
            if from_or_to == 'from':
                e_fund_variety = e_variation.find(".//fund[category='{}']/out".format(change_dict['associatedFund']))
                flag = -1
            elif from_or_to == 'to':
                e_fund_variety = e_variation.find(".//fund[category='{}']/in".format(change_dict['associatedFund']))
                flag = 1
            else:
                print('未知的收支动作！')
                return
            e_fund_variety.text = str((Decimal(e_fund_variety.text) + Decimal(change_dict['value'])).quantize(Decimal('0.00')))
            self.modifyBalance(change_dict['associatedFund'], Decimal(change_dict['value'])*flag)

    def reversalAssociatedFund(self, e_variation, change_dict, from_or_to):
        """
        Describe: 冲正关联账户

        Args:
            e_variation: Element
            change_dict: dict
            from_or_to: ['from', 'to']
        """
        # print(change_dict['associatedFund'])
        if 'associatedFund' in change_dict and change_dict['associatedFund'] != 'None':
            print('执行了associatedFund冲正，操作为', from_or_to)
            if e_variation.find(".//fund[category='{}']".format(change_dict['associatedFund'])) is None:
                print("冲正记录时异常！！该记录不存在关联账户余额变化")
                return
            if from_or_to == 'from':
                e_fund_variety = e_variation.find(".//fund[category='{}']/out".format(change_dict['associatedFund']))
                flag = 1
            elif from_or_to == 'to':
                e_fund_variety = e_variation.find(".//fund[category='{}']/in".format(change_dict['associatedFund']))
                flag = -1
            else:
                print('未知的收支动作！')
                return
            e_fund_variety.text = str((Decimal(e_fund_variety.text) - Decimal(change_dict['value'])).quantize(Decimal('0.00')))
            self.modifyBalance(change_dict['associatedFund'], Decimal(change_dict['value'])*flag)

    def deleteRecord(self, old_record_dict, date_str, action):
        e_date = self.getSpecificDateElement(date_str)
        if isinstance(e_date, int):
            print("未找到这一天的数据！")
            return False

        if action == 'expense':
            action_path = ".//expenses"
            record_path = """.//expense[@necessity='{}'][@associatedFund='{}'][value='{}'][category='{}'][detail='{}'][describe='{}'][from='{}']""".format(
                old_record_dict['necessity'],
                old_record_dict['associatedFund'],
                old_record_dict['value'],
                old_record_dict['category'],
                old_record_dict['detail'],
                old_record_dict['describe'],
                old_record_dict['from'])
        elif action == 'income':
            action_path = ".//incomes"
            record_path = """.//income[@associatedFund='{}'][value='{}'][category='{}'][detail='{}'][describe='{}'][to='{}']""".format(
                old_record_dict['associatedFund'],
                old_record_dict['value'],
                old_record_dict['category'],
                old_record_dict['detail'],
                old_record_dict['describe'],
                old_record_dict['to'])
        elif action == 'movement':
            action_path = ".//movements"
            record_path = """.//movement[value='{}'][detail='{}'][describe='{}'][from='{}'][to='{}']""".format(
                old_record_dict['value'],
                old_record_dict['detail'],
                old_record_dict['describe'],
                old_record_dict['from'],
                old_record_dict['to'])
        else:
            print("未知的动账操作！！")
            return False
        # print(record_path)

        e_action = e_date.find(action_path)
        e_record = e_action.find(record_path)
        if e_record is None:
            print("未找到待删除的记录")
            return False
        e_action.remove(e_record)

        if action == 'movement':
            self.modifyBalance(old_record_dict['from'], Decimal(old_record_dict['value']))
            self.modifyBalance(old_record_dict['to'], Decimal(old_record_dict['value']) * (-1))
        else:
            self.reversalVariation(old_record_dict, e_date)
        return True

    def updateRecord(self, old_record_dict, new_record_dict, date_str, action):
        e_date = self.getSpecificDateElement(date_str)
        if isinstance(e_date, int):
            print("未找到这一天的数据！")
            return False

        if action == 'expense':
            action_path = ".//expenses"
            record_path = """.//expense[@necessity='{}'][@associatedFund='{}'][value='{}'][category='{}'][detail='{}'][describe='{}'][from='{}']""".format(
                old_record_dict['necessity'],
                old_record_dict['associatedFund'],
                old_record_dict['value'],
                old_record_dict['category'],
                old_record_dict['detail'],
                old_record_dict['describe'],
                old_record_dict['from'])
        elif action == 'income':
            action_path = ".//incomes"
            record_path = """.//income[@associatedFund='{}'][value='{}'][category='{}'][detail='{}'][describe='{}'][to='{}']""".format(
                old_record_dict['associatedFund'],
                old_record_dict['value'],
                old_record_dict['category'],
                old_record_dict['detail'],
                old_record_dict['describe'],
                old_record_dict['to'])
        elif action == 'movement':
            action_path = ".//movements"
            record_path = """.//movement[value='{}'][detail='{}'][describe='{}'][from='{}'][to='{}']""".format(
                old_record_dict['value'],
                old_record_dict['detail'],
                old_record_dict['describe'],
                old_record_dict['from'],
                old_record_dict['to'])
        else:
            print("未知的动账操作！！")
            return False
        # print(record_path)

        e_action = e_date.find(action_path)
        e_record = e_action.find(record_path)
        if e_record is None:
            print("未找到待更新的记录")
            return False

        # 修改了出/入账户、数值则需要冲正
        # 不使用elif的原因：账户转移记录的出/入账户均可能被修改
        reverse_flag = False
        if 'from' in old_record_dict and old_record_dict['from'] != new_record_dict['from']:
            reverse_flag = True
        if 'to' in old_record_dict and old_record_dict['to'] != new_record_dict['to']:
            reverse_flag = True
        if Decimal(old_record_dict['value']) != Decimal(new_record_dict['value']):
            reverse_flag = True
        if reverse_flag:
            # 先冲正原记录数据
            # 在用新数据修改账户变化和余额
            if action == 'movement':
                self.modifyBalance(old_record_dict['from'], Decimal(old_record_dict['value']))
                self.modifyBalance(old_record_dict['to'], Decimal(old_record_dict['value']) * (-1))
                self.modifyBalance(new_record_dict['from'], Decimal(new_record_dict['value']) * (-1))
                self.modifyBalance(new_record_dict['to'], Decimal(new_record_dict['value']))
            else:
                self.reversalVariation(old_record_dict, e_date)
                self.organizeVariation(new_record_dict, e_date)

        # 修改记录数据

        for key in new_record_dict.keys():
            if key == 'necessity':
                e_record.attrib['necessity'] = new_record_dict['necessity']
            elif key == 'associatedFund':
                e_record.attrib['associatedFund'] = new_record_dict['associatedFund']
            else:
                e_record.find(".//"+key).text = str(new_record_dict[key])
        return True

    def writeXMLFile(self, file_path):
        # print(file_path)
        pretty_xml(self.e_dailyAccountBook, '    ', '\n')
        self.xml_tree.write(file_path, encoding='utf-8', xml_declaration=True)

    def getWholeYearRecord(self, year):
        """
        Describe: 获取某一年全年的动账记录

        Args:
            year: str
                年份的四位数字符串，格式为"yyyy"

        Returns: tuple[pandas.Dataframe]
            一个四元元组，按顺序表示支出、收入、移动、账户余额变动记录。
            df_expense的列名如下：[date, necessity, value, category, detail, describe, from, associatedFund]
            df_income的列名如下：[date, value, category, detail, describe, to, associatedFund]
            df_movement的列名如下：[date, value, detail, describe, from, to]
            df_variation的列名如下：[date, category, out, in]
        """
        e_year = self.e_dailyAccountBook.find(".//year[@value='{}']".format(year))
        if e_year is None:
            print(f"该年[{year}]没有动账记录!")
            return None
        # df_expense = pd.DataFrame(columns=['date', 'necessity', 'value', 'category', 'detail', 'describe', 'from', 'associatedFund'])
        # df_income = pd.DataFrame(columns=['date', 'value', 'category', 'detail', 'describe', 'to', 'associatedFund'])
        # df_movement = pd.DataFrame(columns=['date', 'value', 'detail', 'describe', 'from', 'to'])
        # df_variation = pd.DataFrame(columns=['date', 'category', 'out', 'in'])
        expense_dict = {'date': [], 'necessity': [], 'value': [], 'category': [], 'detail': [], 'describe': [], 'from': [], 'associatedFund': []}
        income_dict = {'date': [], 'value': [], 'category': [], 'detail': [], 'describe': [], 'to': [], 'associatedFund': []}
        movement_dict = {'date': [], 'value': [], 'detail': [], 'describe': [], 'from': [], 'to': []}
        variation_dict = {'date': [], 'category': [], 'out': [], 'in': []}
        # 创建一个temp_list用于减少代码量，以便对所有动账类型记录字典添加数据
        temp_dict = {'expenses': expense_dict, 'incomes': income_dict, 'movements': movement_dict, 'variation': variation_dict}
        # 5层循环，有点crazy（😀）
        for e_month in list(e_year):
            for e_day in list(e_month):
                # 拼接日期字符串为"yyyyMMdd"格式
                date_str = year + e_month.attrib['value'] + e_day.attrib['value']
                # 获取取指定日期的所有动账记录
                current_parse_dict = self.parseSpecificDateElement(date_str)
                for action in ['expenses', 'incomes', 'movements', 'variation']:
                    if action in current_parse_dict.keys():
                        record_list = current_parse_dict[action]
                        for record in record_list:
                            temp_dict[action]['date'].append(pd.to_datetime(date_str, format="%Y%m%d"))
                            for key in record:
                                temp_dict[action][key].append(record[key])
        # # 显示所有列
        # pd.set_option('display.max_columns', None)
        # # 显示所有行
        # pd.set_option('display.max_rows', None)
        # # 设置value的显示长度为100，默认为50
        # pd.set_option('display.max_colwidth', 1000)
        # # 字段较多时不换行显示
        # pd.set_option('display.width', 1000)
        # # 对齐显示
        # pd.set_option('display.unicode.ambiguous_as_wide', True)
        # pd.set_option('display.unicode.east_asian_width', True)

        result_list = []
        for value in temp_dict.values():
            result_list.append(pd.DataFrame(data=value))
        return result_list
