#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Linfeng_Bingyi
# @Contact : linfengbingyi@qq.com
# @File    : Chart.py
# @Time    : 2023/11/1 21:16
# @Dsc     : 绘图控件
import time

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QBarSeries, QDateTimeAxis, QValueAxis, QBarCategoryAxis, \
    QBarSet, QPieSlice, QPieSeries
from PySide6.QtGui import QPainter, QPen, QCursor
from PySide6.QtCore import Qt, QDate, QDateTime
from PySide6.QtWidgets import QApplication, QToolTip

import sys
from datetime import datetime
import numpy as np
import pandas as pd


def convertPandasToQDateTime(pd_date: pd.Timestamp):
    """
    Describe: 将pandas中Timestamp类型转换为PySide6中QDateTime类型

    Args:
        pd_date: pd.Timestamp
            待转换的pd.Timestamp类型日期，例如 2023-11-01 00:00:00(类型为datetime64[ns])

    Returns:
        转换后的日期
        example:
        打印后将显示 PySide6.QtCore.QDateTime(2023, 1, 1, 0, 0, 0, 0, 0)
    """
    return QDateTime(pd_date.year, pd_date.month, pd_date.day, pd_date.hour, pd_date.minute, pd_date.second)


def scalingDfByTime(df: pd.DataFrame, time_scale_pattern):
    """
    Describe: 将DataFrame按照时间尺度分组，并计算各组数值总和

    Args:
        df: pd.DataFrame
            待处理的数据
        time_scale_pattern: str['%Y', '%Y-%m']
            时间尺度模式，用于对DataFrame分组

    Returns: pd.DataFrame
        处理后的数据
    """
    if time_scale_pattern not in ['%Y', '%Y-%m']:
        raise ValueError("时间尺度模式的格式错误!!")
    return df.groupby(df['date'].dt.strftime(time_scale_pattern))['value'].sum().reset_index().assign(
        date=lambda x: pd.to_datetime(x['date']))


class StatisticBarChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.setChart(self.chart)
        # 坐标轴
        self._axisX = None
        self._axisY = None

        # 存入条形图数据集合set的列表(由于更新条形图所用的QBarSeries.clear()方法会销毁QBarSet对象，故此处通过创建list避免被销毁)
        self.bar_set_expense_list = []
        self.bar_set_income_list = []
        self.bar_set_net_list = []
        # 条形图序列series
        self.bar_series = QBarSeries()
        # x轴时间尺度
        self.time_scale_now = "month"
        self.time_scale = {"year": "yyyy", "month": "yyyy/MM", "week": "", "day": "MM/dd"}

        self.initWidget()
        self.bindSignal()

    def initWidget(self):
        # 标题和标签
        self.chart.setTitle("总额统计")
        # self.chart.legend().hide()

        # 初始化图表
        this_year = QDate.currentDate().year()
        df_init_expense = pd.DataFrame(
            {"date": [datetime.strptime(f"{this_year}{i:0>2}01", "%Y%m%d") for i in range(1, 13)], "value": [1500, 1800] * 6})
        df_init_income = pd.DataFrame(
            {"date": [datetime.strptime(f"{this_year}{i:0>2}01", "%Y%m%d") for i in range(1, 13)], "value": [6800, 6500] * 6})
        df_init_net = pd.DataFrame(
            {"date": [datetime.strptime(f"{this_year}{i:0>2}01", "%Y%m%d") for i in range(1, 13)], "value": [5300, 4300] * 6})
        self.updateBarSeries(df_init_expense, df_init_income, df_init_net)
        # 将series添加到chart中
        self.chart.addSeries(self.bar_series)

    def bindSignal(self):
        self.bar_series.hovered.connect(self.onSeriesHovered)

    def onSeriesHovered(self, state, index, bar_set: QBarSet):
        """
        Describe: 鼠标悬停series事件处理函数

        Args:
            state: bool
                表示鼠标是否悬停在series上。鼠标悬停时为True，离开后变为False
            index: int
                表示鼠标当前所悬停的条形，在条形集合中的编号
            bar_set: PySide6.QtCharts.QBarSet
                表示鼠标当前所悬停的条形集合类别
        """
        # print("悬停series的状态：", state)
        if state:
            QToolTip.showText(QCursor.pos(), "%s\n%s\n%s" %
                              (bar_set.label(),
                               self._axisX.categories()[index],
                               bar_set.at(index)))

    def createStatisticBarChartAxes(self, x_label_list, y_range):
        """
        Describe: 创建统计条形图坐标轴

        Args:
            x_label_list: list
                x轴标签列表
            y_range: tuple
                y轴范围
        """
        # 先删除旧坐标轴
        self.chart.removeAxis(self._axisX)
        self.chart.removeAxis(self._axisY)
        # 创建坐标轴
        self._axisX = QBarCategoryAxis()
        self._axisX.append(x_label_list)
        self._axisY = QValueAxis()
        self._axisY.setRange(y_range[0], y_range[1])
        # 加入坐标轴并绑定
        self.chart.addAxis(self._axisX, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self._axisY, Qt.AlignmentFlag.AlignLeft)
        # 绑定series到坐标轴
        self.bar_series.attachAxis(self._axisX)
        self.bar_series.attachAxis(self._axisY)

    def updateBarSeries(self, df_expense, df_income, df_net):
        """
        Describe: 用新数据更新series

        Args:
            df_expense: pandas.DataFrame
                支出数据。只有 'date'、'value' 两个字段，其中 'date' 的值满足主键唯一(即按每个日期计算了当日总额)
            df_income: pandas.DataFrame
                收入数据。字段情况同支出数据
            df_net: pandas.DataFrame
                净收入数据。字段情况同支出数据
        """
        # 清除series
        self.bar_series.clear()
        # 创建QBarSet
        bar_set_expense = QBarSet("支出", self.chart)
        bar_set_expense.append(df_expense['value'].tolist())
        bar_set_income = QBarSet("收入", self.chart)
        bar_set_income.append(df_income['value'].tolist())
        bar_set_net = QBarSet("净收入", self.chart)
        bar_set_net.append(df_net['value'].tolist())
        # print("条形图净收入的数据：", df_net['value'].tolist())
        # 将QBarSet加入series
        self.bar_series.append(bar_set_expense)
        self.bar_series.append(bar_set_income)
        self.bar_series.append(bar_set_net)

    def displayAllBarChart(self, df_expense, df_income, df_net):
        """
        Describe: 展示新条形图

        Args:
            df_expense: pandas.DataFrame
                支出数据。只有 'date'、'value' 两个字段，其中 'date' 的值满足主键唯一(即按每个日期计算了当日总额)
            df_income: pandas.DataFrame
                收入数据。字段情况同支出数据
            df_net: pandas.DataFrame
                净收入数据。字段情况同支出数据
        """
        self.updateBarSeries(df_expense, df_income, df_net)

        # x轴labels
        date_str_list = [convertPandasToQDateTime(date).toString(self.time_scale[self.time_scale_now])
                         for date in df_net['date']]
        # y轴范围
        axis_y_range = (min(0, df_net['value'].min()), max(df_expense['value'].max(), df_income['value'].max()))
        self.createStatisticBarChartAxes(date_str_list, axis_y_range)

    def scalingDfAndDisplay(self, df_expense, df_income, df_net, time_scale):
        """
        Describe: 根据时间尺度调整数据，并展示结果

        Args:
            df_expense: pandas.DataFrame
                支出数据。只有 'date'、'value' 两个字段，其中 'date' 的值满足主键唯一(即按每个日期计算了当日总额)
            df_income: pandas.DataFrame
                收入数据。字段情况同支出数据
            df_net: pandas.DataFrame
                净收入数据。字段情况同支出数据
            time_scale: str['year', 'month', 'day']
                时间尺度
        """
        if time_scale not in ['year', 'month', 'day']:
            print("不支持的时间尺度!!")
            raise AttributeError("不支持的时间尺度!!")
        # print("传入的时间尺度为：", time_scale)
        self.time_scale_now = time_scale
        #  如果是天数尺度，直接展示
        if time_scale == 'day':
            self.displayAllBarChart(df_expense, df_income, df_net)
            return
        # 根据时间尺度调整数据
        # 默认为月尺度
        group_by_pattern = '%Y-%m'
        if time_scale == 'year':
            group_by_pattern = '%Y'
        df_expense = scalingDfByTime(df_expense, group_by_pattern)
        df_income = scalingDfByTime(df_income, group_by_pattern)
        df_net = scalingDfByTime(df_net, group_by_pattern)
        # print("根据时间尺度调整后的数据：")
        # print(df_expense)
        # print(df_net)
        self.displayAllBarChart(df_expense, df_income, df_net)


class StatisticChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.chart = QChart()
        self.setChart(self.chart)
        # 坐标轴
        self._axisX = None
        self._axisY = None

        # 折线图序列
        self.series_line_expense = QLineSeries()
        self.series_line_income = QLineSeries()
        self.series_line_net = QLineSeries()
        self.series_0_refer = QLineSeries()
        self.list_series_line = [self.series_line_expense, self.series_line_income, self.series_line_net]
        # x轴时间尺度
        self.time_scale_now = "month"
        self.time_scale = {"year": "yyyy年", "month": "yyyy/MM", "week": "", "day": "MM/dd"}

        self.initWidget()
        self.bindSignal()

    def initWidget(self):
        # 标题和标签
        self.chart.setTitle("总额统计")
        # self.chart.legend().hide()

        # 图例名称
        self.series_line_expense.setName("支出")
        self.series_line_income.setName("收入")
        self.series_line_net.setName("净收入")
        # 绑定series到QChart
        for series in self.list_series_line:
            self.chart.addSeries(series)

        # 初始化图表
        this_year = QDate.currentDate().year()
        df_init_expense = pd.DataFrame(
            {"date": [datetime.strptime(f"{this_year}{i:0>2}01", "%Y%m%d") for i in range(1, 13)], "value": [1500, 1800] * 6})
        df_init_income = pd.DataFrame(
            {"date": [datetime.strptime(f"{this_year}{i:0>2}01", "%Y%m%d") for i in range(1, 13)], "value": [6800, 6500] * 6})
        df_init_net = pd.DataFrame(
            {"date": [datetime.strptime(f"{this_year}{i:0>2}01", "%Y%m%d") for i in range(1, 13)], "value": [5300, 4300] * 6})
        self.displayAllLineChart(df_init_expense, df_init_income, df_init_net)

    def bindSignal(self):
        self.series_line_expense.hovered.connect(self.onSeriesHovered)
        self.series_line_income.hovered.connect(self.onSeriesHovered)
        self.series_line_net.hovered.connect(self.onSeriesHovered)

    def onSeriesHovered(self, point, state):
        """
        Describe: 鼠标悬停series事件处理函数

        Args:
            point: QPointF
                表示鼠标悬停的点的坐标
            state: bool
                表示鼠标是否悬停在series上。鼠标悬停时为True，离开后变为False
        """
        # print("悬停series的状态：", state)
        if state:
            # 获取发送者序列的名字
            name = self.sender().name()
            QToolTip.showText(QCursor.pos(), "%s\n%s\n%s" %
                              (name,
                               QDateTime.fromMSecsSinceEpoch(np.int64(point.x())).toString(self.time_scale[self.time_scale_now]),
                               point.y()))

    def createStatisticChartAxis(self, x_count, x_range, y_range):
        """
        Describe: 更新series后需要重新创建坐标轴标轴，这样才能展示出新的series;
                  又因为x轴类型为QDateTimeAxis，无法直接调用QChart.createDefaultAxes()方法创建坐标轴，
                  因此需要自行实现该方法

        Args:
            x_count: int
                x轴刻度线数量
            x_range: tuple[QDateTime]
                x轴范围
            y_range: tuple[float]
                y轴范围
        """
        # 先删除旧坐标轴
        self.chart.removeAxis(self._axisX)
        self.chart.removeAxis(self._axisY)
        # 创建x轴
        self._axisX = QDateTimeAxis()
        self._axisX.setRange(x_range[0], x_range[1])
        self._axisX.setTickCount(x_count)
        self._axisX.setFormat(self.time_scale[self.time_scale_now])
        # 创建y轴
        self._axisY = QValueAxis()
        self._axisY.setRange(y_range[0], y_range[1])
        # 将新坐标轴与QChart和series绑定
        self.chart.addAxis(self._axisX, Qt.AlignBottom)
        self.chart.addAxis(self._axisY, Qt.AlignLeft)
        for series in self.list_series_line:
            series.attachAxis(self._axisX)
            series.attachAxis(self._axisY)

        # 显示地展示y=0参考线
        series_refer = self.series_0_refer
        series_refer.clear()
        series_refer.setName("0刻度线")
        series_refer.setPen(QPen(Qt.black))
        series_refer.append(np.int64(x_range[0].toMSecsSinceEpoch()), 0)
        series_refer.append(np.int64(x_range[1].toMSecsSinceEpoch()), 0)
        self.chart.addSeries(series_refer)
        series_refer.attachAxis(self._axisX)
        series_refer.attachAxis(self._axisY)

    def updateLineSeries(self, df, series):
        """
        Describe: 用新数据更新series

        Args:
            df: pandas.DataFrame
                数据源，包含date和value两列
            series: QLineSeries
                待更新的series
        """
        series.clear()
        for i in range(len(df)):
            datetime_int64 = np.int64(convertPandasToQDateTime(df["date"][i]).toMSecsSinceEpoch())
            series.append(datetime_int64, df["value"][i])

    def displayAllLineChart(self, df_expense, df_income, df_net):
        """
        Describe: 用新数据更新所有折线图

        Args:
            df_expense: pandas.DataFrame
                支出数据。只有 'date'、'value' 两个字段，其中 'date' 的值满足主键唯一(即按每个日期计算了当日总额)
            df_income: pandas.DataFrame
                收入数据。字段情况同支出数据
            df_net: pandas.DataFrame
                净收入数据。字段情况同支出数据
        """
        # 更新series
        self.updateLineSeries(df_expense, self.series_line_expense)
        self.updateLineSeries(df_income, self.series_line_income)
        self.updateLineSeries(df_net, self.series_line_net)
        # 获取坐标轴范围
        axisX_range = (convertPandasToQDateTime(df_expense['date'].min()),
                       convertPandasToQDateTime(df_expense['date'].max()))
        axisY_range = (min(0, df_net['value'].min()), max(df_expense['value'].max(), df_income['value'].max()))
        # 更新坐标轴并与QChart、QXYSeries绑定
        self.createStatisticChartAxis(len(df_expense), axisX_range, axisY_range)

    def scalingDfAndDisplay(self, df_expense, df_income, df_net, time_scale):
        """
        Describe: 根据时间尺度调整数据，并展示结果

        Args:
            df_expense: pandas.DataFrame
                支出数据。只有 'date'、'value' 两个字段，其中 'date' 的值满足主键唯一(即按每个日期计算了当日总额)
            df_income: pandas.DataFrame
                收入数据。字段情况同支出数据
            df_net: pandas.DataFrame
                净收入数据。字段情况同支出数据
            time_scale: str['year', 'month', 'day']
                时间尺度
        """
        if time_scale not in ['year', 'month', 'day']:
            print("不支持的时间尺度!!")
            raise AttributeError("不支持的时间尺度!!")
        print("传入的时间尺度为：", time_scale)
        self.time_scale_now = time_scale
        #  如果是天数尺度，直接展示
        if time_scale == 'day':
            self.displayAllLineChart(df_expense, df_income, df_net)
            return
        # 根据时间尺度调整数据
        # 默认为月尺度
        group_by_pattern = '%Y-%m'
        if time_scale == 'year':
            group_by_pattern = '%Y'
        df_expense = scalingDfByTime(df_expense, group_by_pattern)
        df_income = scalingDfByTime(df_income, group_by_pattern)
        df_net = scalingDfByTime(df_net, group_by_pattern)
        print("根据时间尺度调整后的数据：")
        print(df_expense)
        print(df_income)
        self.displayAllLineChart(df_expense, df_income, df_net)
        
        
class ActionStructurePieChartView(QChartView):
    def __init__(self, action, parent=None):
        super().__init__()
        if action not in ['expense', 'income']:
            raise AttributeError("创建收支结构饼图时，传入的动账类型错误!!")
        self.action = action                                                   # 动账类型
        self.action_localization_dict = {'expense': '支出', 'income': '收入'}    # 动账类型翻译字典
        self.action_localized = self.action_localization_dict[action]          # 翻译后的动账类型，用于在界面上展示
        self.parent = parent

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.setChart(self.chart)

        # 饼图切片slice列表
        self.slice_expense_list = []
        self.slice_income_list = []
        # 饼图序列series
        self.pie_series = QPieSeries()
        self.pie_series.setHoleSize(0.4)

        self.initWidget()
        self.bindSignal()

    def initWidget(self):
        # 标题和标签
        self.chart.setTitle(self.action_localized + "结构")
        # self.chart.legend().hide()

        category_init_dict = {i: self.action_localized + str(i + 1) for i in range(5)}
        df_init_action = pd.DataFrame(
            {"category": [i for i in range(5)], "value": [(i + 2) * 10 for i in range(5)]})
        self.updatePieSeries(df_init_action, category_init_dict)
        # 将series添加到chart中
        self.chart.addSeries(self.pie_series)

    def bindSignal(self):
        self.pie_series.hovered.connect(self.onSeriesHovered)

    def onSeriesHovered(self, the_slice: QPieSlice, state):
        """
        Describe: 鼠标悬停series事件处理函数

        Args:
            the_slice: PySide6.QtCharts.QPieSlice
                表示鼠标当前所悬停的饼图切片
            state: bool
                表示鼠标是否悬停在slice上。鼠标悬停时为True，离开后变为False
        """
        the_slice.setExploded(state)
        the_slice.setLabelVisible(state)
        the_slice.setLabelArmLengthFactor(0.03)
        pure_label = the_slice.label().split(' ')[0]
        if state:
            the_slice.setLabel(f'{pure_label} {the_slice.value()} {the_slice.percentage():.2%}')
        else:
            the_slice.setLabel(pure_label)

    def updatePieSeries(self, df_action, category_dict):
        """
        Describe: 用新数据更新series

        Args:
            df_action: pandas.DataFrame
                动账数据。只有 'category'、'value' 两个字段
            category_dict: dict
                收支类型字典
        """
        # 清除series
        self.pie_series.clear()
        # print("饼图数据：\n", df_action)
        # 将数据加入series
        for i in range(len(df_action)):
            category_text = category_dict[df_action['category'][i]]
            self.pie_series.append(category_text, df_action['value'][i])

    def displayFoldAnimation(self):
        """
        Describe: 展示收起动画效果
        """
        # print("收起动画")
        self.pie_series.setPieEndAngle(0)

    def displayExpandAnimation(self):
        """
        Describe: 展示展开动画效果
        """
        # print("展开动画")
        self.pie_series.setPieEndAngle(360)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    chart_view = ActionStructurePieChartView("expense")
    chart_view.setRenderHint(QPainter.Antialiasing)
    chart_view.show()

    sys.exit(app.exec())
