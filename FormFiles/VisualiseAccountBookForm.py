from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QDate
from CustomWidgets import ActionStructurePieChartView

import pandas as pd
from decimal import Decimal

from FormFiles.VisualiseAccountBook import Ui_VisualiseAccountBook
from FileProcess.AccountBookXML import AccountBookXMLProcessor

from CommonFiles.ConstArgs import *


def formatDateStrToDf(date_str):
    """
    Describe: 使日期格式与Dataframe日期格式保持一致

    Args:
        date_str: str
            日期字符串，格式为yyyyMMdd

    Returns: str
        格式为yyyy-MM-dd
    """
    return pd.to_datetime(date_str, format="%Y%m%d")


class WidgetVisualiseAccountBook(QWidget, Ui_VisualiseAccountBook):

    def __init__(self):
        super(WidgetVisualiseAccountBook, self).__init__()
        self.setupUi(self)
        # 初始化收支结构tab中的图表。由于__init__函数需要传参，因此不能通过QDesigner的“提升为”功能去初始化
        self.expense_pie = ActionStructurePieChartView('expense')
        self.income_pie = ActionStructurePieChartView('income')
        self.gridLayout_pie_chart.addWidget(self.expense_pie, 1, 0)
        self.gridLayout_pie_chart.addWidget(self.income_pie, 2, 0)
        self.ex_or_in_struct_chart.setVisible(False)
        self.income_pie.setVisible(False)

        self.flag_expand_config_area = True                             # 判断总额统计tab的图表配置区域是否展开
        self.flag_df_updated = False                                    # 判断总额统计tab的df是否已经更新
        self.file_processor: AccountBookXMLProcessor = None             # 收支记录文件读写器
        self.whole_year_records = {}                                    # 全年记录
        self.balance_list = []                                          # 存款账户余额列表
        self.tab_ExOrIn_time_scale_format = {'year': "yyyy", 'month': "yyyy/MM", 'day': "MM/dd"}
        self.current_pie_date = None                                    # 收支结构tab饼图当前日期

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
        # 初始化时仅获取今年的所有记录，当日期范围包含其他年份时再扩展
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

        # 设置记录表头
        self.tableWidget_fund_sum.setColumnCount(len(fundConst.TABLEWIDGET_COLUMN_HEAD))
        self.tableWidget_fund_sum.setHorizontalHeaderLabels(list(fundConst.TABLEWIDGET_COLUMN_HEAD))

        # 展示总额统计tab页中相关数据与图表
        self.updateTabStatistic()

        # 收支结构tab--------------------------------------------
        # 设置初始日期范围为本月
        self.dateEdit_end_date_tab_pie.setDate(self.today_date)
        self.dateEdit_start_date_tab_pie.setDate(self.today_month_1st)
        # 设置饼图标题日期范围为本月
        self.current_pie_date = self.today_date
        self.label_current_range_pie.setText(self.current_pie_date.toString(self.tab_ExOrIn_time_scale_format['month']))
        # 设置收入饼图初始状态为收起
        self.income_pie.displayFoldAnimation()

        # 展示收支结构tab页中相关数据与图表
        self.updateTabExOrInStructure()

    def bindSignal(self):
        # 总额统计tab--------------------------------------------
        self.pushButton_expand_config_area.clicked.connect(self.changeStatisticChartExpand)
        self.dateEdit_start_date.dateChanged.connect(self.updateTabStatistic)
        self.dateEdit_end_date.dateChanged.connect(self.updateTabStatistic)
        self.radioButton_day_scale.clicked.connect(self.updateTabStatistic)
        self.radioButton_month_scale.clicked.connect(self.updateTabStatistic)
        self.radioButton_year_scale.clicked.connect(self.updateTabStatistic)
        # 收支结构tab--------------------------------------------
        self.dateEdit_start_date_tab_pie.dateChanged.connect(self.updateTabExOrInStructure)
        self.dateEdit_end_date_tab_pie.dateChanged.connect(self.updateTabExOrInStructure)
        self.radioButton_day_scale_tab_pie.clicked.connect(self.updateTabExOrInStructure)
        self.radioButton_month_scale_tab_pie.clicked.connect(self.updateTabExOrInStructure)
        self.radioButton_year_scale_tab_pie.clicked.connect(self.updateTabExOrInStructure)
        self.radioButton_expense_tab_pie.clicked.connect(self.showTabExOrInPie)
        self.radioButton_income_tab_pie.clicked.connect(self.showTabExOrInPie)

    def changeStatisticChartExpand(self):
        """
        Describe: 控制总额统计tab的图表配置区域是否展开
        """
        self.flag_expand_config_area = not self.flag_expand_config_area
        self.widget_config_panel.setVisible(self.flag_expand_config_area)
        if self.flag_expand_config_area:    # 展开
            self.pushButton_expand_config_area.setText(">")
            self.widget_chart_config.setMinimumWidth(150)
            self.pushButton_expand_config_area.setMinimumHeight(30)
        else:                               # 隐藏
            self.pushButton_expand_config_area.setText("<")
            self.widget_chart_config.setMinimumWidth(35)
            self.pushButton_expand_config_area.setMinimumHeight(350)

    def getCurrentDateRange(self, tab='statistic'):
        """
        Describe: 返回标签页中当前选择的日期范围

        Args:
            tab: str['statistic', 'pie']
                目标标签页。'statistic' 表示总额统计页，'pie' 表示收支结构页

        Returns: tuple[str, str]
            包含起始日期、结束日期的二元元组，格式为yyyyMMdd
            example:
                ('20200101', '20200131')
        """
        date_edit_start = self.dateEdit_start_date if tab == 'statistic' else self.dateEdit_start_date_tab_pie
        date_edit_end = self.dateEdit_end_date if tab == 'statistic' else self.dateEdit_end_date_tab_pie
        return date_edit_start.text().replace('/', ''), date_edit_end.text().replace('/', '')

    def updateTabStatistic(self):
        """
        Describe: 响应时间选择控件，更新总额统计tab页所有信息
        """
        start_date, end_date = self.getCurrentDateRange()
        if start_date > end_date:
            print("结束日期小于起始日期!!")
            return
        self.display_all_sum(start_date, end_date)
        self.displayFundSumTable(start_date, end_date)
        self.displayStatisticChart(start_date, end_date, self.getTimeScale())

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
        action_df = self.whole_year_records[action]
        # 根据日期和类型筛选动账记录
        filtered_df = action_df.loc[(action_df['date'].between(start_date, end_date)) &
                                    (action_df['category'].isin(ignore_category) == False)]   # 此处与False比较必须用双等号
        # 如果指定了账户，则筛选该账户的动账记录
        if fund is not None:
            from_or_to = 'from' if action == 'expense' else 'to'
            filtered_df = filtered_df.loc[filtered_df[from_or_to] == fund]
        return filtered_df['value'].sum()

    def getTotalBalance(self):
        """
        Describe: 计算存款账户余额总和

        Returns: float
            存款账户余额总和
        """
        total_balance = Decimal(0.00)
        for balance_fund in self.balance_list:
            if not balance_fund['ignore']:
                total_balance += Decimal(balance_fund['value']).quantize(Decimal('0.00'))
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

    def getTimeScale(self):
        """
        Describe: 获取当前选中的时间尺度

        Returns: str['year', 'month', 'day']
            表示时间尺度的字符串，'year' 表示年度，'month' 表示月度，'day' 表示日度
        """
        if self.radioButton_year_scale.isChecked():
            return 'year'
        elif self.radioButton_month_scale.isChecked():
            return 'month'
        elif self.radioButton_day_scale.isChecked():
            return 'day'
        else:
            print("未选择时间尺度!!")
            raise AttributeError("未选择时间尺度!!")

    def displayStatisticChart(self, start_date, end_date, time_scale):
        # 获取日期范围内的收支记录数据
        start_date = formatDateStrToDf(start_date)
        end_date = formatDateStrToDf(end_date)
        ex_ignore_category = expenseConst.IGNORE_CATEGORY
        in_ignore_category = incomeConst.IGNORE_CATEGORY
        ex_df = self.whole_year_records['expense']
        in_df = self.whole_year_records['income']
        df_expense = ex_df.loc[(ex_df['date'].between(start_date, end_date)) &
                               (ex_df['category'].isin(ex_ignore_category) == False)].loc[:, ['date', 'value']]
        df_income = in_df.loc[(in_df['date'].between(start_date, end_date)) &
                              (in_df['category'].isin(in_ignore_category) == False)].loc[:, ['date', 'value']]

        # 按日分组收支记录，得到每日总的收入与支出，以便计算每日净收入
        df_expense_grouped = df_expense.groupby('date').sum().reset_index()
        df_income_grouped = df_income.groupby('date').sum().reset_index()
        # 根据支出Dataframe与收入Dataframe进行join操作，以便得到净收入收入Dataframe
        df_net = df_expense_grouped.set_index('date').join(df_income_grouped.set_index('date'), rsuffix='_income', how='outer')
        # 新增一列df_net.value，其值为df_income.value减去df_expense.value
        df_net['value'] = df_net['value_income'].sub(df_net['value'], fill_value=0)
        # 按date字段join后，date则变成了index，此时只需提取value字段
        df_net = df_net[['value']]
        # 重命名index为date，并将其从index设为column
        df_net.index.name = 'date'
        df_net = df_net.reset_index()

        # print("仅保留两个字段后的收入数据\n", df_income)
        # print("净收入数据\n", df_net)
        self.statistic_chart.scalingDfAndDisplay(df_expense_grouped, df_income_grouped, df_net, time_scale)

    def updateTabExOrInStructure(self):
        """
        Describe: 响应各控件，并根据时间尺度控制饼图的时间范围。更新收支结构tab页所有信息
        """
        start_date, end_date = self.getCurrentDateRange('pie')
        if start_date > end_date:
            print("结束日期{}小于起始日期{}!!".format(end_date, start_date))
            return
        time_scale = self.getPieTimeScale()
        # 更新饼图时间范围标签
        self.label_current_range_pie.setText(self.current_pie_date.toString(self.tab_ExOrIn_time_scale_format[time_scale]))
        # 更新饼图
        self.displayExOrInStructureChart(start_date, end_date)

    def getPieTimeScale(self):
        """
        Describe: 获取Pie标签页中，当前选中的时间尺度

        Returns: str['year', 'month', 'day']
            表示时间尺度的字符串，'year' 表示年度，'month' 表示月度，'day' 表示日度
        """
        if self.radioButton_year_scale_tab_pie.isChecked():
            return 'year'
        elif self.radioButton_month_scale_tab_pie.isChecked():
            return 'month'
        elif self.radioButton_day_scale_tab_pie.isChecked():
            return 'day'
        else:
            print("未选择时间尺度!!")
            raise AttributeError("未选择时间尺度!!")

    def getPieTimeInterval(self, refer_date, time_scale):
        """
        Describe: 根据参考日期和时间尺度返回天数

        Args:
            refer_date: str
                日期字符串，格式为yyyyMMdd
            time_scale: str['year', 'month', 'day']
                时间尺度

        Returns: int
            对应时间尺度的间隔天数
            example:
            当time_scale为'month'，refer_date为'20240201'时，表示获取2024年2月的天数
        """
        if time_scale == 'year':
            year = int(refer_date[0:4])
            return 365 if ((year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0))) else 366
        elif time_scale == 'month':
            dt_refer_date = QDate(int(refer_date[0:4]), int(refer_date[4:6]), int(refer_date[6:8]))
            return dt_refer_date.daysInMonth()
        elif time_scale == 'day':
            return 1
        else:
            print("不支持的时间尺度!!")
            raise AttributeError("不支持的时间尺度!!")

    def getNextReferDate(self, refer_date, time_scale):
        """
        Describe: 根据参考日期和时间尺度，返回下一个参考日期

        Args:
            refer_date: str
                日期字符串，格式为yyyyMMdd
            time_scale: str['year', 'month', 'day']
                时间尺度

        Returns: str
            下一个参考日期
        """
        dt_refer_date = QDate(int(refer_date[0:4]), int(refer_date[4:6]), int(refer_date[6:8]))
        dt_refer_date.addDays(self.getPieTimeInterval(refer_date, time_scale))
        return str(refer_date)

    def displayExOrInStructureChart(self, start_date, end_date):
        # 获取日期范围内的收支记录数据
        start_date = formatDateStrToDf(start_date)
        end_date = formatDateStrToDf(end_date)
        ex_ignore_category = expenseConst.IGNORE_CATEGORY
        in_ignore_category = incomeConst.IGNORE_CATEGORY
        ex_df = self.whole_year_records['expense']
        in_df = self.whole_year_records['income']
        df_expense = ex_df.loc[(ex_df['date'].between(start_date, end_date)) &
                               (ex_df['category'].isin(ex_ignore_category) == False)].loc[:, ['value', 'category']]
        df_income = in_df.loc[(in_df['date'].between(start_date, end_date)) &
                              (in_df['category'].isin(in_ignore_category) == False)].loc[:, ['value', 'category']]

        # 按日分组收支记录，得到每日总的收入与支出，以便计算每日净收入
        df_expense_grouped = df_expense.groupby('category').sum().reset_index()
        df_income_grouped = df_income.groupby('category').sum().reset_index()

        self.expense_pie.updatePieSeries(df_expense_grouped, expenseConst.CATEGORY)
        self.income_pie.updatePieSeries(df_income_grouped, incomeConst.CATEGORY)

    def showTabExOrInPie(self):
        if self.radioButton_expense_tab_pie.isChecked():
            self.income_pie.displayFoldAnimation()
            self.expense_pie.setVisible(True)
            self.income_pie.setVisible(False)
            self.expense_pie.displayExpandAnimation()
        else:
            self.expense_pie.displayFoldAnimation()
            self.expense_pie.setVisible(False)
            self.income_pie.setVisible(True)
            self.income_pie.displayExpandAnimation()
