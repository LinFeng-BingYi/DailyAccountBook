#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Linfeng_Bingyi
# @Contact : linfengbingyi@qq.com
# @File    : TestCustomWidget.py
# @Time    : 2023/10/1 15:38
# @Dsc     : 测试自定义组件

from PySide6.QtWidgets import QApplication, QWidget, QGridLayout

import CustomWidgets


if __name__ == '__main__':
    app = QApplication([])
    myWidget = QWidget()
    gridLayout_global = QGridLayout(myWidget)

    # 测试的控件
    testWidget = CustomWidgets.ComboBoxInTableWidget({}, None)

    gridLayout_global.addWidget(testWidget)
    myWidget.show()
    app.exec()
