# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VisualiseAccountBook.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDateEdit,
    QFrame, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from CustomWidgets import StatisticBarChartView

class Ui_VisualiseAccountBook(object):
    def setupUi(self, VisualiseAccountBook):
        if not VisualiseAccountBook.objectName():
            VisualiseAccountBook.setObjectName(u"VisualiseAccountBook")
        VisualiseAccountBook.resize(951, 600)
        self.gridLayout_top = QGridLayout(VisualiseAccountBook)
        self.gridLayout_top.setSpacing(0)
        self.gridLayout_top.setObjectName(u"gridLayout_top")
        self.gridLayout_top.setContentsMargins(0, 0, 0, 0)
        self.widget_general = QWidget(VisualiseAccountBook)
        self.widget_general.setObjectName(u"widget_general")
        self.gridLayout_general = QGridLayout(self.widget_general)
        self.gridLayout_general.setSpacing(0)
        self.gridLayout_general.setObjectName(u"gridLayout_general")
        self.gridLayout_general.setContentsMargins(0, 5, 0, 0)
        self.tabWidget_general = QTabWidget(self.widget_general)
        self.tabWidget_general.setObjectName(u"tabWidget_general")
        self.tabWidget_general.setTabPosition(QTabWidget.West)
        self.tab_statistic = QWidget()
        self.tab_statistic.setObjectName(u"tab_statistic")
        self.gridLayout_statistic_top = QGridLayout(self.tab_statistic)
        self.gridLayout_statistic_top.setSpacing(0)
        self.gridLayout_statistic_top.setObjectName(u"gridLayout_statistic_top")
        self.gridLayout_statistic_top.setContentsMargins(5, 5, 5, 5)
        self.widget_statistic = QWidget(self.tab_statistic)
        self.widget_statistic.setObjectName(u"widget_statistic")
        self.verticalLayout_statistic_general = QVBoxLayout(self.widget_statistic)
        self.verticalLayout_statistic_general.setSpacing(5)
        self.verticalLayout_statistic_general.setObjectName(u"verticalLayout_statistic_general")
        self.verticalLayout_statistic_general.setContentsMargins(0, 0, 0, 0)
        self.widget_date_range = QWidget(self.widget_statistic)
        self.widget_date_range.setObjectName(u"widget_date_range")
        self.horizontalLayout_date_range = QHBoxLayout(self.widget_date_range)
        self.horizontalLayout_date_range.setSpacing(5)
        self.horizontalLayout_date_range.setObjectName(u"horizontalLayout_date_range")
        self.horizontalLayout_date_range.setContentsMargins(0, 0, 0, 0)
        self.label_start_date = QLabel(self.widget_date_range)
        self.label_start_date.setObjectName(u"label_start_date")
        self.label_start_date.setMaximumSize(QSize(80, 16777215))
        self.label_start_date.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_date_range.addWidget(self.label_start_date)

        self.dateEdit_start_date = QDateEdit(self.widget_date_range)
        self.dateEdit_start_date.setObjectName(u"dateEdit_start_date")
        self.dateEdit_start_date.setMinimumSize(QSize(30, 30))
        self.dateEdit_start_date.setCalendarPopup(True)

        self.horizontalLayout_date_range.addWidget(self.dateEdit_start_date)

        self.label_end_date = QLabel(self.widget_date_range)
        self.label_end_date.setObjectName(u"label_end_date")
        self.label_end_date.setMaximumSize(QSize(80, 16777215))
        self.label_end_date.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_date_range.addWidget(self.label_end_date)

        self.dateEdit_end_date = QDateEdit(self.widget_date_range)
        self.dateEdit_end_date.setObjectName(u"dateEdit_end_date")
        self.dateEdit_end_date.setMinimumSize(QSize(30, 30))
        self.dateEdit_end_date.setCalendarPopup(True)

        self.horizontalLayout_date_range.addWidget(self.dateEdit_end_date)


        self.verticalLayout_statistic_general.addWidget(self.widget_date_range)

        self.widget_expense_and_income_statistic = QWidget(self.widget_statistic)
        self.widget_expense_and_income_statistic.setObjectName(u"widget_expense_and_income_statistic")
        self.horizontalLayout_exps_incm_statistic = QHBoxLayout(self.widget_expense_and_income_statistic)
        self.horizontalLayout_exps_incm_statistic.setSpacing(5)
        self.horizontalLayout_exps_incm_statistic.setObjectName(u"horizontalLayout_exps_incm_statistic")
        self.horizontalLayout_exps_incm_statistic.setContentsMargins(0, 0, 0, 0)
        self.widget_value_sum = QWidget(self.widget_expense_and_income_statistic)
        self.widget_value_sum.setObjectName(u"widget_value_sum")
        self.gridLayout_value_sum = QGridLayout(self.widget_value_sum)
        self.gridLayout_value_sum.setSpacing(2)
        self.gridLayout_value_sum.setObjectName(u"gridLayout_value_sum")
        self.gridLayout_value_sum.setContentsMargins(0, 0, 0, 0)
        self.label_expense_sum = QLabel(self.widget_value_sum)
        self.label_expense_sum.setObjectName(u"label_expense_sum")
        self.label_expense_sum.setMinimumSize(QSize(80, 0))
        self.label_expense_sum.setAlignment(Qt.AlignCenter)

        self.gridLayout_value_sum.addWidget(self.label_expense_sum, 0, 0, 1, 1)

        self.label_expense_sum_value = QLabel(self.widget_value_sum)
        self.label_expense_sum_value.setObjectName(u"label_expense_sum_value")
        font = QFont()
        font.setFamilies([u"Magneto"])
        font.setPointSize(20)
        font.setBold(True)
        self.label_expense_sum_value.setFont(font)

        self.gridLayout_value_sum.addWidget(self.label_expense_sum_value, 0, 1, 1, 1)

        self.label_income_sum = QLabel(self.widget_value_sum)
        self.label_income_sum.setObjectName(u"label_income_sum")
        self.label_income_sum.setMinimumSize(QSize(80, 0))
        self.label_income_sum.setAlignment(Qt.AlignCenter)

        self.gridLayout_value_sum.addWidget(self.label_income_sum, 1, 0, 1, 1)

        self.label_income_sum_value = QLabel(self.widget_value_sum)
        self.label_income_sum_value.setObjectName(u"label_income_sum_value")
        self.label_income_sum_value.setFont(font)

        self.gridLayout_value_sum.addWidget(self.label_income_sum_value, 1, 1, 1, 1)

        self.label_net_income_sum = QLabel(self.widget_value_sum)
        self.label_net_income_sum.setObjectName(u"label_net_income_sum")
        self.label_net_income_sum.setMinimumSize(QSize(80, 0))
        self.label_net_income_sum.setAlignment(Qt.AlignCenter)

        self.gridLayout_value_sum.addWidget(self.label_net_income_sum, 2, 0, 1, 1)

        self.label_net_income_sum_value = QLabel(self.widget_value_sum)
        self.label_net_income_sum_value.setObjectName(u"label_net_income_sum_value")
        self.label_net_income_sum_value.setFont(font)

        self.gridLayout_value_sum.addWidget(self.label_net_income_sum_value, 2, 1, 1, 1)

        self.label_total_assets_sum = QLabel(self.widget_value_sum)
        self.label_total_assets_sum.setObjectName(u"label_total_assets_sum")
        self.label_total_assets_sum.setMinimumSize(QSize(80, 0))
        self.label_total_assets_sum.setAlignment(Qt.AlignCenter)

        self.gridLayout_value_sum.addWidget(self.label_total_assets_sum, 3, 0, 1, 1)

        self.label_total_assets_sum_value = QLabel(self.widget_value_sum)
        self.label_total_assets_sum_value.setObjectName(u"label_total_assets_sum_value")
        self.label_total_assets_sum_value.setFont(font)

        self.gridLayout_value_sum.addWidget(self.label_total_assets_sum_value, 3, 1, 1, 1)

        self.gridLayout_value_sum.setColumnStretch(0, 1)
        self.gridLayout_value_sum.setColumnStretch(1, 3)

        self.horizontalLayout_exps_incm_statistic.addWidget(self.widget_value_sum)

        self.widget_fund_sum = QWidget(self.widget_expense_and_income_statistic)
        self.widget_fund_sum.setObjectName(u"widget_fund_sum")
        self.verticalLayout_fund_sum = QVBoxLayout(self.widget_fund_sum)
        self.verticalLayout_fund_sum.setSpacing(0)
        self.verticalLayout_fund_sum.setObjectName(u"verticalLayout_fund_sum")
        self.verticalLayout_fund_sum.setContentsMargins(2, 2, 2, 2)
        self.tableWidget_fund_sum = QTableWidget(self.widget_fund_sum)
        self.tableWidget_fund_sum.setObjectName(u"tableWidget_fund_sum")
        self.tableWidget_fund_sum.setFrameShadow(QFrame.Plain)
        self.tableWidget_fund_sum.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_fund_sum.setAlternatingRowColors(True)
        self.tableWidget_fund_sum.setSortingEnabled(True)
        self.tableWidget_fund_sum.setRowCount(0)
        self.tableWidget_fund_sum.setColumnCount(0)
        self.tableWidget_fund_sum.horizontalHeader().setVisible(True)
        self.tableWidget_fund_sum.verticalHeader().setVisible(True)

        self.verticalLayout_fund_sum.addWidget(self.tableWidget_fund_sum)


        self.horizontalLayout_exps_incm_statistic.addWidget(self.widget_fund_sum)

        self.horizontalLayout_exps_incm_statistic.setStretch(0, 1)
        self.horizontalLayout_exps_incm_statistic.setStretch(1, 2)

        self.verticalLayout_statistic_general.addWidget(self.widget_expense_and_income_statistic)

        self.widget_chart_area = QWidget(self.widget_statistic)
        self.widget_chart_area.setObjectName(u"widget_chart_area")
        self.horizontalLayout_chart_area = QHBoxLayout(self.widget_chart_area)
        self.horizontalLayout_chart_area.setSpacing(5)
        self.horizontalLayout_chart_area.setObjectName(u"horizontalLayout_chart_area")
        self.horizontalLayout_chart_area.setContentsMargins(0, 0, 0, 0)
        self.widget_chart_display = QWidget(self.widget_chart_area)
        self.widget_chart_display.setObjectName(u"widget_chart_display")
        self.gridLayout_chart_display = QGridLayout(self.widget_chart_display)
        self.gridLayout_chart_display.setSpacing(0)
        self.gridLayout_chart_display.setObjectName(u"gridLayout_chart_display")
        self.gridLayout_chart_display.setContentsMargins(0, 7, 0, 0)
        self.statistic_chart = StatisticBarChartView(self.widget_chart_display)
        self.statistic_chart.setObjectName(u"statistic_chart")

        self.gridLayout_chart_display.addWidget(self.statistic_chart, 0, 0, 1, 1)


        self.horizontalLayout_chart_area.addWidget(self.widget_chart_display)

        self.widget_chart_config = QWidget(self.widget_chart_area)
        self.widget_chart_config.setObjectName(u"widget_chart_config")
        self.widget_chart_config.setMinimumSize(QSize(150, 0))
        self.verticalLayout_chart_config = QVBoxLayout(self.widget_chart_config)
        self.verticalLayout_chart_config.setSpacing(0)
        self.verticalLayout_chart_config.setObjectName(u"verticalLayout_chart_config")
        self.verticalLayout_chart_config.setContentsMargins(0, 0, 0, 0)
        self.widget_config_panel = QWidget(self.widget_chart_config)
        self.widget_config_panel.setObjectName(u"widget_config_panel")
        self.verticalLayout_config_panel = QVBoxLayout(self.widget_config_panel)
        self.verticalLayout_config_panel.setSpacing(0)
        self.verticalLayout_config_panel.setObjectName(u"verticalLayout_config_panel")
        self.verticalLayout_config_panel.setContentsMargins(0, 0, 0, 0)
        self.groupBox_time_scale = QGroupBox(self.widget_config_panel)
        self.groupBox_time_scale.setObjectName(u"groupBox_time_scale")
        self.groupBox_time_scale.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_time_scale.setFlat(True)
        self.gridLayout_time_scale = QGridLayout(self.groupBox_time_scale)
        self.gridLayout_time_scale.setSpacing(5)
        self.gridLayout_time_scale.setObjectName(u"gridLayout_time_scale")
        self.gridLayout_time_scale.setContentsMargins(0, 0, 0, 0)
        self.radioButton_day_scale = QRadioButton(self.groupBox_time_scale)
        self.radioButton_day_scale.setObjectName(u"radioButton_day_scale")

        self.gridLayout_time_scale.addWidget(self.radioButton_day_scale, 0, 0, 1, 1)

        self.radioButton_month_scale = QRadioButton(self.groupBox_time_scale)
        self.radioButton_month_scale.setObjectName(u"radioButton_month_scale")
        self.radioButton_month_scale.setChecked(True)

        self.gridLayout_time_scale.addWidget(self.radioButton_month_scale, 0, 1, 1, 1)

        self.radioButton_year_scale = QRadioButton(self.groupBox_time_scale)
        self.radioButton_year_scale.setObjectName(u"radioButton_year_scale")

        self.gridLayout_time_scale.addWidget(self.radioButton_year_scale, 1, 0, 1, 1)


        self.verticalLayout_config_panel.addWidget(self.groupBox_time_scale)

        self.groupBox_chart_item = QGroupBox(self.widget_config_panel)
        self.groupBox_chart_item.setObjectName(u"groupBox_chart_item")
        self.groupBox_chart_item.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_chart_item.setFlat(True)
        self.gridLayout_chart_iten = QGridLayout(self.groupBox_chart_item)
        self.gridLayout_chart_iten.setSpacing(5)
        self.gridLayout_chart_iten.setObjectName(u"gridLayout_chart_iten")
        self.gridLayout_chart_iten.setContentsMargins(0, 0, 0, 0)
        self.checkBox_net_income = QCheckBox(self.groupBox_chart_item)
        self.checkBox_net_income.setObjectName(u"checkBox_net_income")
        self.checkBox_net_income.setChecked(True)

        self.gridLayout_chart_iten.addWidget(self.checkBox_net_income, 2, 0, 1, 1)

        self.checkBox_expense = QCheckBox(self.groupBox_chart_item)
        self.checkBox_expense.setObjectName(u"checkBox_expense")
        self.checkBox_expense.setChecked(True)

        self.gridLayout_chart_iten.addWidget(self.checkBox_expense, 0, 0, 1, 1)

        self.checkBox_income = QCheckBox(self.groupBox_chart_item)
        self.checkBox_income.setObjectName(u"checkBox_income")
        self.checkBox_income.setChecked(True)

        self.gridLayout_chart_iten.addWidget(self.checkBox_income, 0, 1, 1, 1)


        self.verticalLayout_config_panel.addWidget(self.groupBox_chart_item)

        self.verticalLayout_config_panel.setStretch(0, 5)
        self.verticalLayout_config_panel.setStretch(1, 5)

        self.verticalLayout_chart_config.addWidget(self.widget_config_panel)

        self.pushButton_expand_config_area = QPushButton(self.widget_chart_config)
        self.pushButton_expand_config_area.setObjectName(u"pushButton_expand_config_area")

        self.verticalLayout_chart_config.addWidget(self.pushButton_expand_config_area)

        self.verticalLayout_chart_config.setStretch(0, 6)
        self.verticalLayout_chart_config.setStretch(1, 1)

        self.horizontalLayout_chart_area.addWidget(self.widget_chart_config)

        self.horizontalLayout_chart_area.setStretch(0, 100)
        self.horizontalLayout_chart_area.setStretch(1, 1)

        self.verticalLayout_statistic_general.addWidget(self.widget_chart_area)

        self.verticalLayout_statistic_general.setStretch(0, 1)
        self.verticalLayout_statistic_general.setStretch(1, 4)
        self.verticalLayout_statistic_general.setStretch(2, 8)

        self.gridLayout_statistic_top.addWidget(self.widget_statistic, 2, 0, 1, 1)

        self.tabWidget_general.addTab(self.tab_statistic, "")
        self.tab_pie_display = QWidget()
        self.tab_pie_display.setObjectName(u"tab_pie_display")
        self.tab_pie_display.setMinimumSize(QSize(922, 589))
        self.gridLayout_pie_top = QGridLayout(self.tab_pie_display)
        self.gridLayout_pie_top.setSpacing(0)
        self.gridLayout_pie_top.setObjectName(u"gridLayout_pie_top")
        self.gridLayout_pie_top.setContentsMargins(5, 5, 5, 5)
        self.widget_pie_display = QWidget(self.tab_pie_display)
        self.widget_pie_display.setObjectName(u"widget_pie_display")
        self.horizontalLayout_pie_general = QHBoxLayout(self.widget_pie_display)
        self.horizontalLayout_pie_general.setSpacing(5)
        self.horizontalLayout_pie_general.setObjectName(u"horizontalLayout_pie_general")
        self.horizontalLayout_pie_general.setContentsMargins(0, 0, 0, 0)
        self.widget_display = QWidget(self.widget_pie_display)
        self.widget_display.setObjectName(u"widget_display")
        self.verticalLayout_display = QVBoxLayout(self.widget_display)
        self.verticalLayout_display.setSpacing(0)
        self.verticalLayout_display.setObjectName(u"verticalLayout_display")
        self.verticalLayout_display.setContentsMargins(0, 0, 0, 0)
        self.widget_pie_control_bar = QWidget(self.widget_display)
        self.widget_pie_control_bar.setObjectName(u"widget_pie_control_bar")
        self.horizontalLayout_pie_control_bar = QHBoxLayout(self.widget_pie_control_bar)
        self.horizontalLayout_pie_control_bar.setSpacing(0)
        self.horizontalLayout_pie_control_bar.setObjectName(u"horizontalLayout_pie_control_bar")
        self.horizontalLayout_pie_control_bar.setContentsMargins(0, 0, 0, 0)
        self.pushButton_prev_range_pie = QPushButton(self.widget_pie_control_bar)
        self.pushButton_prev_range_pie.setObjectName(u"pushButton_prev_range_pie")
        self.pushButton_prev_range_pie.setMinimumSize(QSize(0, 30))
        self.pushButton_prev_range_pie.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_pie_control_bar.addWidget(self.pushButton_prev_range_pie)

        self.label_current_range_pie = QLabel(self.widget_pie_control_bar)
        self.label_current_range_pie.setObjectName(u"label_current_range_pie")
        font1 = QFont()
        font1.setPointSize(15)
        self.label_current_range_pie.setFont(font1)
        self.label_current_range_pie.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_pie_control_bar.addWidget(self.label_current_range_pie)

        self.pushButton_post_range_pie = QPushButton(self.widget_pie_control_bar)
        self.pushButton_post_range_pie.setObjectName(u"pushButton_post_range_pie")
        self.pushButton_post_range_pie.setMinimumSize(QSize(0, 30))
        self.pushButton_post_range_pie.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_pie_control_bar.addWidget(self.pushButton_post_range_pie)

        self.horizontalLayout_pie_control_bar.setStretch(0, 1)
        self.horizontalLayout_pie_control_bar.setStretch(1, 16)
        self.horizontalLayout_pie_control_bar.setStretch(2, 1)

        self.verticalLayout_display.addWidget(self.widget_pie_control_bar)

        self.widget_pie_chart = QWidget(self.widget_display)
        self.widget_pie_chart.setObjectName(u"widget_pie_chart")
        self.gridLayout_pie_chart = QGridLayout(self.widget_pie_chart)
        self.gridLayout_pie_chart.setSpacing(0)
        self.gridLayout_pie_chart.setObjectName(u"gridLayout_pie_chart")
        self.gridLayout_pie_chart.setContentsMargins(0, 0, 0, 0)
        self.ex_or_in_struct_chart = QGraphicsView(self.widget_pie_chart)
        self.ex_or_in_struct_chart.setObjectName(u"ex_or_in_struct_chart")

        self.gridLayout_pie_chart.addWidget(self.ex_or_in_struct_chart, 0, 0, 1, 1)


        self.verticalLayout_display.addWidget(self.widget_pie_chart)

        self.verticalLayout_display.setStretch(0, 1)
        self.verticalLayout_display.setStretch(1, 12)

        self.horizontalLayout_pie_general.addWidget(self.widget_display)

        self.widget_control_panel = QWidget(self.widget_pie_display)
        self.widget_control_panel.setObjectName(u"widget_control_panel")
        self.verticalLayout_control_panel = QVBoxLayout(self.widget_control_panel)
        self.verticalLayout_control_panel.setSpacing(2)
        self.verticalLayout_control_panel.setObjectName(u"verticalLayout_control_panel")
        self.verticalLayout_control_panel.setContentsMargins(0, 0, 0, 0)
        self.groupBox_date_range = QGroupBox(self.widget_control_panel)
        self.groupBox_date_range.setObjectName(u"groupBox_date_range")
        self.groupBox_date_range.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_date_range.setFlat(True)
        self.gridLayout_date_range = QGridLayout(self.groupBox_date_range)
        self.gridLayout_date_range.setSpacing(5)
        self.gridLayout_date_range.setObjectName(u"gridLayout_date_range")
        self.gridLayout_date_range.setContentsMargins(0, 0, 0, 0)
        self.label_start_date_tab_pie = QLabel(self.groupBox_date_range)
        self.label_start_date_tab_pie.setObjectName(u"label_start_date_tab_pie")
        self.label_start_date_tab_pie.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_date_range.addWidget(self.label_start_date_tab_pie, 0, 0, 1, 1)

        self.dateEdit_start_date_tab_pie = QDateEdit(self.groupBox_date_range)
        self.dateEdit_start_date_tab_pie.setObjectName(u"dateEdit_start_date_tab_pie")
        self.dateEdit_start_date_tab_pie.setMinimumSize(QSize(0, 30))
        self.dateEdit_start_date_tab_pie.setCalendarPopup(True)

        self.gridLayout_date_range.addWidget(self.dateEdit_start_date_tab_pie, 0, 1, 1, 1)

        self.label_end_date_tab_pie = QLabel(self.groupBox_date_range)
        self.label_end_date_tab_pie.setObjectName(u"label_end_date_tab_pie")
        self.label_end_date_tab_pie.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_date_range.addWidget(self.label_end_date_tab_pie, 1, 0, 1, 1)

        self.dateEdit_end_date_tab_pie = QDateEdit(self.groupBox_date_range)
        self.dateEdit_end_date_tab_pie.setObjectName(u"dateEdit_end_date_tab_pie")
        self.dateEdit_end_date_tab_pie.setMinimumSize(QSize(0, 30))
        self.dateEdit_end_date_tab_pie.setCalendarPopup(True)

        self.gridLayout_date_range.addWidget(self.dateEdit_end_date_tab_pie, 1, 1, 1, 1)


        self.verticalLayout_control_panel.addWidget(self.groupBox_date_range)

        self.groupBox_time_scale_tab_pie = QGroupBox(self.widget_control_panel)
        self.groupBox_time_scale_tab_pie.setObjectName(u"groupBox_time_scale_tab_pie")
        self.groupBox_time_scale_tab_pie.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_time_scale_tab_pie.setFlat(True)
        self.gridLayout_time_scale_tab_pie = QGridLayout(self.groupBox_time_scale_tab_pie)
        self.gridLayout_time_scale_tab_pie.setSpacing(5)
        self.gridLayout_time_scale_tab_pie.setObjectName(u"gridLayout_time_scale_tab_pie")
        self.gridLayout_time_scale_tab_pie.setContentsMargins(0, 0, 0, 0)
        self.radioButton_day_scale_tab_pie = QRadioButton(self.groupBox_time_scale_tab_pie)
        self.radioButton_day_scale_tab_pie.setObjectName(u"radioButton_day_scale_tab_pie")

        self.gridLayout_time_scale_tab_pie.addWidget(self.radioButton_day_scale_tab_pie, 0, 0, 1, 1)

        self.radioButton_month_scale_tab_pie = QRadioButton(self.groupBox_time_scale_tab_pie)
        self.radioButton_month_scale_tab_pie.setObjectName(u"radioButton_month_scale_tab_pie")
        self.radioButton_month_scale_tab_pie.setChecked(True)

        self.gridLayout_time_scale_tab_pie.addWidget(self.radioButton_month_scale_tab_pie, 0, 1, 1, 1)

        self.radioButton_year_scale_tab_pie = QRadioButton(self.groupBox_time_scale_tab_pie)
        self.radioButton_year_scale_tab_pie.setObjectName(u"radioButton_year_scale_tab_pie")

        self.gridLayout_time_scale_tab_pie.addWidget(self.radioButton_year_scale_tab_pie, 1, 0, 1, 1)


        self.verticalLayout_control_panel.addWidget(self.groupBox_time_scale_tab_pie)

        self.groupBox_vary_type = QGroupBox(self.widget_control_panel)
        self.groupBox_vary_type.setObjectName(u"groupBox_vary_type")
        self.groupBox_vary_type.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_vary_type.setFlat(True)
        self.gridLayout_vary_type = QGridLayout(self.groupBox_vary_type)
        self.gridLayout_vary_type.setSpacing(5)
        self.gridLayout_vary_type.setObjectName(u"gridLayout_vary_type")
        self.gridLayout_vary_type.setContentsMargins(0, 0, 0, 0)
        self.radioButton_expense_tab_pie = QRadioButton(self.groupBox_vary_type)
        self.radioButton_expense_tab_pie.setObjectName(u"radioButton_expense_tab_pie")
        self.radioButton_expense_tab_pie.setChecked(True)

        self.gridLayout_vary_type.addWidget(self.radioButton_expense_tab_pie, 0, 0, 1, 1)

        self.radioButton_income_tab_pie = QRadioButton(self.groupBox_vary_type)
        self.radioButton_income_tab_pie.setObjectName(u"radioButton_income_tab_pie")

        self.gridLayout_vary_type.addWidget(self.radioButton_income_tab_pie, 0, 1, 1, 1)


        self.verticalLayout_control_panel.addWidget(self.groupBox_vary_type)

        self.groupBox_filter_fund = QGroupBox(self.widget_control_panel)
        self.groupBox_filter_fund.setObjectName(u"groupBox_filter_fund")
        self.groupBox_filter_fund.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_filter_fund.setFlat(True)
        self.verticalLayout_filter_fund = QVBoxLayout(self.groupBox_filter_fund)
        self.verticalLayout_filter_fund.setSpacing(5)
        self.verticalLayout_filter_fund.setObjectName(u"verticalLayout_filter_fund")
        self.verticalLayout_filter_fund.setContentsMargins(5, 10, 5, 0)
        self.tableWidget = QTableWidget(self.groupBox_filter_fund)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_filter_fund.addWidget(self.tableWidget)


        self.verticalLayout_control_panel.addWidget(self.groupBox_filter_fund)

        self.verticalLayout_control_panel.setStretch(0, 4)
        self.verticalLayout_control_panel.setStretch(1, 3)
        self.verticalLayout_control_panel.setStretch(2, 2)
        self.verticalLayout_control_panel.setStretch(3, 14)

        self.horizontalLayout_pie_general.addWidget(self.widget_control_panel)

        self.horizontalLayout_pie_general.setStretch(0, 5)
        self.horizontalLayout_pie_general.setStretch(1, 2)

        self.gridLayout_pie_top.addWidget(self.widget_pie_display, 0, 0, 1, 1)

        self.tabWidget_general.addTab(self.tab_pie_display, "")

        self.gridLayout_general.addWidget(self.tabWidget_general, 0, 0, 1, 1)


        self.gridLayout_top.addWidget(self.widget_general, 0, 0, 1, 1)


        self.retranslateUi(VisualiseAccountBook)

        self.tabWidget_general.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(VisualiseAccountBook)
    # setupUi

    def retranslateUi(self, VisualiseAccountBook):
        VisualiseAccountBook.setWindowTitle(QCoreApplication.translate("VisualiseAccountBook", u"\u53ef\u89c6\u5316\u8d26\u672c", None))
        self.label_start_date.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u8d77\u59cb\u65e5\u671f", None))
        self.dateEdit_start_date.setDisplayFormat(QCoreApplication.translate("VisualiseAccountBook", u"yyyy/MM/dd", None))
        self.label_end_date.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u7ed3\u675f\u65e5\u671f", None))
        self.dateEdit_end_date.setDisplayFormat(QCoreApplication.translate("VisualiseAccountBook", u"yyyy/MM/dd", None))
        self.label_expense_sum.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u652f\u51fa", None))
        self.label_expense_sum_value.setText(QCoreApplication.translate("VisualiseAccountBook", u"123456789.00", None))
        self.label_income_sum.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u6536\u5165", None))
        self.label_income_sum_value.setText(QCoreApplication.translate("VisualiseAccountBook", u"123456789.00", None))
        self.label_net_income_sum.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u51c0\u6536\u5165", None))
        self.label_net_income_sum_value.setText(QCoreApplication.translate("VisualiseAccountBook", u"123456789.00", None))
        self.label_total_assets_sum.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u603b\u8d44\u4ea7", None))
        self.label_total_assets_sum_value.setText(QCoreApplication.translate("VisualiseAccountBook", u"123456789.00", None))
        self.groupBox_time_scale.setTitle(QCoreApplication.translate("VisualiseAccountBook", u"\u65f6\u95f4\u5c3a\u5ea6", None))
        self.radioButton_day_scale.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u65e5\u53f7", None))
        self.radioButton_month_scale.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u6708\u4efd", None))
        self.radioButton_year_scale.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u5e74\u4efd", None))
        self.groupBox_chart_item.setTitle(QCoreApplication.translate("VisualiseAccountBook", u"\u56fe\u8868\u5143\u7d20", None))
        self.checkBox_net_income.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u51c0\u6536\u5165", None))
        self.checkBox_expense.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u652f\u51fa", None))
        self.checkBox_income.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u6536\u5165", None))
        self.pushButton_expand_config_area.setText(QCoreApplication.translate("VisualiseAccountBook", u">", None))
        self.tabWidget_general.setTabText(self.tabWidget_general.indexOf(self.tab_statistic), QCoreApplication.translate("VisualiseAccountBook", u"\u603b\u989d\u7edf\u8ba1", None))
        self.pushButton_prev_range_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"<", None))
        self.label_current_range_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"2023/11/18", None))
        self.pushButton_post_range_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u">", None))
        self.groupBox_date_range.setTitle(QCoreApplication.translate("VisualiseAccountBook", u"\u65f6\u95f4\u8303\u56f4", None))
        self.label_start_date_tab_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u8d77\u59cb\u65e5\u671f", None))
        self.dateEdit_start_date_tab_pie.setDisplayFormat(QCoreApplication.translate("VisualiseAccountBook", u"yyyy/MM/dd", None))
        self.label_end_date_tab_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u7ed3\u675f\u65e5\u671f", None))
        self.dateEdit_end_date_tab_pie.setDisplayFormat(QCoreApplication.translate("VisualiseAccountBook", u"yyyy/MM/dd", None))
        self.groupBox_time_scale_tab_pie.setTitle(QCoreApplication.translate("VisualiseAccountBook", u"\u65f6\u95f4\u5c3a\u5ea6", None))
        self.radioButton_day_scale_tab_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u65e5\u53f7", None))
        self.radioButton_month_scale_tab_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u6708\u4efd", None))
        self.radioButton_year_scale_tab_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u5e74\u4efd", None))
        self.groupBox_vary_type.setTitle(QCoreApplication.translate("VisualiseAccountBook", u"\u52a8\u8d26\u7c7b\u578b", None))
        self.radioButton_expense_tab_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u652f\u51fa", None))
        self.radioButton_income_tab_pie.setText(QCoreApplication.translate("VisualiseAccountBook", u"\u6536\u5165", None))
        self.groupBox_filter_fund.setTitle(QCoreApplication.translate("VisualiseAccountBook", u"\u5b58\u6b3e\u8d26\u6237", None))
        self.tabWidget_general.setTabText(self.tabWidget_general.indexOf(self.tab_pie_display), QCoreApplication.translate("VisualiseAccountBook", u"\u6536\u652f\u7ed3\u6784", None))
    # retranslateUi

