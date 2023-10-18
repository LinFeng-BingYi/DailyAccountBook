from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QDate

from FormFiles.VisualiseAccountBook import Ui_VisualiseAccountBook
from FileProcess.AccountBookXML import AccountBookXMLProcessor

from CommonFiles.MyConstArgs import *


class WidgetVisualiseAccountBook(QWidget, Ui_VisualiseAccountBook):

    def __init__(self):
        super(WidgetVisualiseAccountBook, self).__init__()
        self.setupUi(self)

        self.flag_expand_config_area = True             # 统计tab的图表配置区域是否展开

        self.today_date = QDate.currentDate()                                       # 今天的日期
        self.today_month_1st = self.today_date.addDays(-self.today_date.day() + 1)  # 本月第一天
        self.today_year_1st = QDate(self.today_date.year(), 1, 1)                   # 本年第一天
        # print("今天的日期、本月第一天、本年第一天：", self.today_date, self.today_month_1st, self.today_year_1st)

        self.initWidgets()
        self.bindSignal()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def initWidgets(self):
        # 统计tab--------------------------------------------
        # 设置初始日期范围为本月
        self.dateEdit_end_date.setDate(self.today_date)
        self.dateEdit_start_date.setDate(self.today_month_1st)

        # 饼图tab--------------------------------------------
        # 设置初始日期范围为本月
        self.dateEdit_end_date_tab_pie.setDate(self.today_date)
        self.dateEdit_start_date_tab_pie.setDate(self.today_month_1st)
        # 设置饼图标题日期范围为本月
        self.label_current_range_pie.setText(self.today_date.toString('yyyy/MM/XX'))

    def bindSignal(self):
        self.pushButton_expand_config_area.clicked.connect(self.changeStatisticChartExpand)

    def changeStatisticChartExpand(self):
        """
        Describe: 控制统计tab的图表配置区域是否展开

        """
        self.flag_expand_config_area = not self.flag_expand_config_area
        self.widget_config_panel.setVisible(self.flag_expand_config_area)
        if self.flag_expand_config_area:    # 展开
            self.widget_chart_config.setMinimumWidth(150)
            self.pushButton_expand_config_area.setMinimumHeight(30)
        else:                               # 隐藏
            self.widget_chart_config.setMinimumWidth(35)
            self.pushButton_expand_config_area.setMinimumHeight(350)
