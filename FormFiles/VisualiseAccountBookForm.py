from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QDate

import pandas as pd
from datetime import datetime

from FormFiles.VisualiseAccountBook import Ui_VisualiseAccountBook
from FileProcess.AccountBookXML import AccountBookXMLProcessor

from CommonFiles.ConstArgs import *

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def formatDateStrToDf(date_str):
    """
    Describe: 使日期格式与Dataframe日期格式保持一致

    Args:
        date_str: str
            日期字符串，格式为yyyyMMdd

    Returns: str
        格式为yyyy-MM-dd
    """
    return datetime.strptime(date_str, "%Y%m%d").date()


class WidgetVisualiseAccountBook(QWidget, Ui_VisualiseAccountBook):

    def __init__(self):
        super(WidgetVisualiseAccountBook, self).__init__()
        self.setupUi(self)

        self.flag_expand_config_area = True                             # 判断总额统计tab的图表配置区域是否展开
        self.flag_df_updated = False                                    # 判断总额统计tab的df是否已经更新
        self.file_processor: AccountBookXMLProcessor = None             # 收支记录文件读写器
        self.whole_year_records = {}                                    # 全年记录
        self.balance_list = []                                          # 存款账户余额列表

        self.today_date = QDate.currentDate()                                       # 今天的日期
        self.today_month_1st = self.today_date.addDays(-self.today_date.day() + 1)  # 本月第一天
        self.today_year_1st = QDate(self.today_date.year(), 1, 1)                   # 本年第一天
        # print("今天的日期、本月第一天、本年第一天：", self.today_date, self.today_month_1st, self.today_year_1st)

        self.initWidgets()
        self.bindSignal()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def initWidgets(self):
        # 初始化本窗口的文件处理器
        self.file_processor = AccountBookXMLProcessor(commonConst.ACCOUNT_BOOK_PATH)
        result = self.file_processor.getWholeYearRecord(str(self.today_date.year()))
        self.whole_year_records['expense'] = result[0]
        self.whole_year_records['income'] = result[1]
        self.whole_year_records['movement'] = result[2]
        self.whole_year_records['variation'] = result[3]
        self.balance_list = self.file_processor.parseBalance()

        # 总额统计tab--------------------------------------------
        # 设置初始日期范围为本月
        self.dateEdit_end_date.setDate(self.today_date)
        self.dateEdit_start_date.setDate(self.today_month_1st)

        # 显示总和区
        self.display_all_sum(self.today_month_1st.toString("yyyyMMdd"), self.today_date.toString("yyyyMMdd"))

        # 设置记录表头
        self.tableWidget_fund_sum.setColumnCount(len(fundConst.TABLEWIDGET_COLUMN_HEAD))
        self.tableWidget_fund_sum.setHorizontalHeaderLabels(list(fundConst.TABLEWIDGET_COLUMN_HEAD))
        self.displayFundSumTable(self.today_month_1st.toString("yyyyMMdd"), self.today_date.toString("yyyyMMdd"))

        # 收支结构tab--------------------------------------------
        # 设置初始日期范围为本月
        self.dateEdit_end_date_tab_pie.setDate(self.today_date)
        self.dateEdit_start_date_tab_pie.setDate(self.today_month_1st)
        # 设置饼图标题日期范围为本月
        self.label_current_range_pie.setText(self.today_date.toString('yyyy/MM/XX'))

    def bindSignal(self):
        self.pushButton_expand_config_area.clicked.connect(self.changeStatisticChartExpand)
        self.dateEdit_start_date.dateChanged.connect(lambda: self.display_all_sum(self.dateEdit_start_date.text().replace('/', ''), self.dateEdit_end_date.text().replace('/', '')))
        self.dateEdit_end_date.dateChanged.connect(lambda: self.display_all_sum(self.dateEdit_start_date.text().replace('/', ''), self.dateEdit_end_date.text().replace('/', '')))

    def changeStatisticChartExpand(self):
        """
        Describe: 控制总额统计tab的图表配置区域是否展开
        """
        self.flag_expand_config_area = not self.flag_expand_config_area
        self.widget_config_panel.setVisible(self.flag_expand_config_area)
        if self.flag_expand_config_area:    # 展开
            self.widget_chart_config.setMinimumWidth(150)
            self.pushButton_expand_config_area.setMinimumHeight(30)
        else:                               # 隐藏
            self.widget_chart_config.setMinimumWidth(35)
            self.pushButton_expand_config_area.setMinimumHeight(350)

    def getCurrentDateRange(self):
        """
        Describe: 返回当前选择的日期范围

        Returns: tuple[str, str]
            包含起始日期、结束日期的二元元组，格式为yyyyMMdd
            example:
                ('20200101', '20200131')
        """
        return self.dateEdit_start_date.text().replace('/', ''), self.dateEdit_end_date.text().replace('/', '')

    def display_all_sum(self, start_date, end_date):
        """
        Describe: 显示总额统计tab的总和区

        Args:
            start_date: str
                起始日期，格式为yyyyMMdd
            end_date: str
                结束日期，格式为yyyyMMdd
        """
        if end_date < start_date:
            print("结束日期小于起始日期!!")
            return
        # 若更新过Dataframe，则先排序
        if self.flag_df_updated:
            for df in self.whole_year_records.values():
                df = df.sort_values(by='date')
            self.flag_df_updated = False
        total_expense_value = self.getRangeExpenseOrIncome(start_date, end_date, 'expense', expenseConst)
        total_income_value = self.getRangeExpenseOrIncome(start_date, end_date, 'income', incomeConst)
        self.label_expense_sum_value.setText(str(total_expense_value))
        self.label_income_sum_value.setText(str(total_income_value))
        self.label_net_income_sum_value.setText(str(total_income_value - total_expense_value))
        self.label_total_assets_sum_value.setText(str(self.getTotalBalance()))

    def getRangeExpenseOrIncome(self, start_date, end_date, action, constClass, fund=None):
        """
        Describe: 计算范围内支出或收入总和

        Args:
            start_date: str
                起始日期，格式为yyyyMMdd
            end_date: str
                结束日期，格式为yyyyMMdd
            action: str
                'expense' or 'income'
            constClass: class
                expenseConst or incomeConst
            fund: int
                动账账户，不指定则查找全部

        Returns: float
            支出或收入总和

        Raises:
            ValueError:
                action参数错误
        """
        if action not in ['expense', 'income']:
            raise ValueError("action参数错误")
        start_date = formatDateStrToDf(start_date)
        end_date = formatDateStrToDf(end_date)
        # print("正在计算支出总和，范围：", start_date, " to ", end_date)
        ignore_category = constClass.IGNORE_CATEGORY
        query_str = '(date >= @start_date) & (date <= @end_date) & (category not in @ignore_category)'
        if fund is not None:
            from_or_to = 'from' if action == 'expense' else 'to'
            query_str = query_str + ' & (`' + from_or_to + '` == @fund)'
        return self.whole_year_records[action].query(query_str)['value'].sum()

    def getTotalBalance(self):
        """
        Describe: 计算存款账户余额总和

        Returns: float
            存款账户余额总和
        """
        total_balance = 0
        for balance_fund in self.balance_list:
            if not balance_fund['ignore']:
                total_balance += balance_fund['value']
        return total_balance

    def displayFundSumTable(self, start_date, end_date):
        self.tableWidget_fund_sum.setRowCount(0)
        self.tableWidget_fund_sum.setRowCount(len(self.balance_list))

        current_row = 0
        for fund in self.balance_list:
            self.tableWidget_fund_sum.setItem(current_row, 0, QTableWidgetItem(fund['fundName']))
            self.tableWidget_fund_sum.setItem(current_row, 1, QTableWidgetItem(str(fund['value'])))
            current_fund_expense = self.getRangeExpenseOrIncome(start_date, end_date, 'expense', expenseConst, fund['category'])
            self.tableWidget_fund_sum.setItem(current_row, 2, QTableWidgetItem(str(current_fund_expense)))
            current_fund_income = self.getRangeExpenseOrIncome(start_date, end_date, 'income', incomeConst, fund['category'])
            self.tableWidget_fund_sum.setItem(current_row, 3, QTableWidgetItem(str(current_fund_income)))
            self.tableWidget_fund_sum.setItem(current_row, 4, QTableWidgetItem(str(fund['ignore'])))
            current_row += 1
