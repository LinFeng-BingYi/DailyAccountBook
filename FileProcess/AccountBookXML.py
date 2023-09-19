#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Linfeng_Bingyi
# @Contact : linfengbingyi@qq.com
# @File    : AccountBookXML.py
# @Time    : 2023/9/9 16:40
from xml.etree import ElementTree as et
import os
from decimal import Decimal


def pretty_xml(element, indent, newline='\n', level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
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

            若未找到指定year，则返回int类型的0；若未找到指定month，则返回int类型的1；若未找到指定day，则返回int类型的2
        """
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
            balance_dict = {"value": float(e_fund.find('.//value').text),
                            "category": int(e_fund.find('.//category').text),
                            "fundName": e_fund.find('.//fundName').text}
            balance_list.append(balance_dict)
        return balance_list

    def parseSpecificDateElement(self, date_str):
        e_date = self.getSpecificDateElement(date_str)

        if isinstance(e_date, int):
            print("未找到这一天的数据！")
            return None

        parse_dict = dict()

        for child_node in list(e_date):
            print(child_node.tag)
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
                print("未知类型的节点名")

        return parse_dict

    def parseExpense(self, e_expense):
        expense_dict = {
            'necessity': True if (e_expense.attrib['necessity'].lower() == 'true') else False,
            'value': float(e_expense.find('.//value').text),
            'category': int(e_expense.find('.//category').text),
            'detail': e_expense.find('.//detail').text,
            'describe': e_expense.find('.//describe').text,
            'from': int(e_expense.find('.//from').text),
            'associatedFund': int(e_expense.attrib['associatedFund']) if (
                    ('associatedFund' in e_expense.attrib) and e_expense.attrib['associatedFund'] != 'None') else None
        }

        return expense_dict

    def parseIncome(self, e_income):
        income_dict = {
            'associatedFund': int(e_income.attrib['associatedFund']) if (
                    ('associatedFund' in e_income.attrib) and e_income.attrib['associatedFund'] != 'None') else None,
            'value': float(e_income.find('.//value').text),
            'category': int(e_income.find('.//category').text),
            'detail': e_income.find('.//detail').text,
            'describe': e_income.find('.//describe').text,
            'to': int(e_income.find('.//to').text)
        }

        return income_dict

    def parseMovement(self, e_movement):
        movement_dict = {
            'value': float(e_movement.find('.//value').text),
            'detail': e_movement.find('.//detail').text,
            'describe': e_movement.find('.//describe').text,
            'from': int(e_movement.find('.//from').text),
            'to': int(e_movement.find('.//to').text)
        }

        return movement_dict

    def parseVariation(self, e_fund):
        fund_dict = {
            'category': int(e_fund.find('.//category').text),
            'out': float(e_fund.find('.//out').text),
            'in': float(e_fund.find('.//in').text),
        }

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

        if 'necessity' in expense_dict:
            e_expense.set('necessity', expense_dict['necessity'])
            del expense_dict['necessity']
        if 'associatedFund' in expense_dict:
            e_expense.set('associatedFund', expense_dict['associatedFund'])
            del expense_dict['associatedFund']
        for key, value in expense_dict.items():
            self.createChildElement(e_expense, key, value)

        print(et.tostring(e_expenses, 'utf8'))

    def organizeIncome(self, income_dict: dict, date_str):
        e_date = self.getSpecificDateElement(date_str)

        if isinstance(e_date, int):
            print("未找到这一天的数据！")

            e_date = self.switch_caseInitStartDate(e_date, date_str)

        e_incomes = e_date.find(".//incomes") if e_date.find(".//incomes") is not None else self.createChildElement(e_date, 'incomes', None)
        e_income = et.SubElement(e_incomes, 'income')

        self.organizeVariation(income_dict, e_date)

        if 'associatedFund' in income_dict:
            e_income.set('associatedFund', income_dict['associatedFund'])
            del income_dict['associatedFund']
        for key, value in income_dict.items():
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

    def organizeAssociatedFund(self, e_variation, change_dict, from_or_to):
        print(change_dict['associatedFund'])
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

    def writeXMLFile(self, file_path):
        print(file_path)
        pretty_xml(self.e_dailyAccountBook, '    ', '\n')
        self.xml_tree.write(file_path, encoding='utf-8', xml_declaration=True)
