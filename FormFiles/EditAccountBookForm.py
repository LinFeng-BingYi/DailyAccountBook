from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QTableWidgetItem
from PySide6.QtCore import Qt, QDate

from CustomWidgets import ComboBoxInTableWidget

import os
from collections import OrderedDict

from FormFiles.EditAccountBook import Ui_EditAccountBook
from FileProcess.AccountBookXML import AccountBookXMLProcessor

from CommonFiles.ConstArgs import *


class WidgetEditAccountBook(QWidget, Ui_EditAccountBook):

    def __init__(self):
        super(WidgetEditAccountBook, self).__init__()
        self.setupUi(self)
        self.tableWidget_expense.setColumnCount(len(expenseConst.TABLEWIDGET_COLUMN_HEAD))
        self.tableWidget_expense.setHorizontalHeaderLabels(list(expenseConst.TABLEWIDGET_COLUMN_HEAD))
        self.tableWidget_income.setColumnCount(len(incomeConst.TABLEWIDGET_COLUMN_HEAD))
        self.tableWidget_income.setHorizontalHeaderLabels(list(incomeConst.TABLEWIDGET_COLUMN_HEAD))
        self.tableWidget_movement.setColumnCount(len(movementConst.TABLEWIDGET_COLUMN_HEAD))
        self.tableWidget_movement.setHorizontalHeaderLabels(list(movementConst.TABLEWIDGET_COLUMN_HEAD))

        self.cwd = os.getcwd()              # 程序当前工作目录
        self.file_processor: AccountBookXMLProcessor = None          # 收支记录文件读写器
        self.file_parse_result = dict()     # 收支记录文件解析结果

        self.initWidgets()
        self.bindSignal()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def bindSignal(self):
        self.pushButton_file_path.clicked.connect(self.chooseFile)
        self.lineEdit_file_path.cursorPositionChanged.connect(self.responseSelectedDateChanging)
        self.dateEdit.dateChanged.connect(self.responseSelectedDateChanging)
        self.groupBox_expense.clicked.connect(lambda: self.widget_expense.setVisible(not self.widget_expense.isVisible()))
        self.groupBox_income.clicked.connect(lambda: self.widget_income.setVisible(not self.widget_income.isVisible()))
        self.groupBox_movement.clicked.connect(lambda: self.widget_movement.setVisible(not self.widget_movement.isVisible()))

    def initWidgets(self):
        self.dateEdit.setDate(QDate.currentDate())

    def chooseFile(self):
        chosen_file, file_type = QFileDialog.getOpenFileName(self, "选择文件", self.cwd, "All Files(*);;XML Files(*.xml)")
        self.lineEdit_file_path.setText(chosen_file)

    def responseSelectedDateChanging(self):
        if not self.lineEdit_file_path.text():
            print("还未选择文件！")
            return
        self.file_processor = AccountBookXMLProcessor(self.lineEdit_file_path.text())
        self.file_parse_result = self.file_processor.parseSpecificDateElement(self.dateEdit.text().replace('/', ''))
        print(self.file_parse_result)
        if self.file_parse_result is None:
            self.file_parse_result = {}

        if 'expenses' not in self.file_parse_result:
            self.file_parse_result['expenses'] = []
        if 'incomes' not in self.file_parse_result:
            self.file_parse_result['incomes'] = []
        if 'movements' not in self.file_parse_result:
            self.file_parse_result['movements'] = []
        if 'variation' not in self.file_parse_result:
            self.file_parse_result['variation'] = []

        self.updateExpenseTable(self.file_parse_result['expenses'])
        self.updateIncomeTable(self.file_parse_result['incomes'])
        self.updateMovementTable(self.file_parse_result['movements'])

    def setExistTableCell(self, tableWidget, current_row, value_dict: dict, const_class):
        """
        Describe: 为已存在记录的表格行设置单元格。根据列名设置对应类型(格式)的单元格

        Args:
            tableWidget: QTableWidget
                涉及的表格
            current_row: int
                本条记录所在行号
            value_dict: dict
                记录字典
            const_class: Union[ExpenseConst, IncomeConst, MovementConst]
                记录类型对应的常量类
        """
        keys_list = list(value_dict.keys())
        for key, value in value_dict.items():
            if key == 'necessity':
                comboBox = ComboBoxInTableWidget(NECESSITY, value)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'value':
                tableWidget.setItem(current_row, keys_list.index(key), QTableWidgetItem(str(value)))
            elif key == 'category':
                comboBox = ComboBoxInTableWidget(const_class.CATEGORY, value)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'detail':
                tableWidget.setItem(current_row, keys_list.index(key), QTableWidgetItem(value))
            elif key == 'describe':
                tableWidget.setItem(current_row, keys_list.index(key), QTableWidgetItem(value))
            elif key == 'from':
                comboBox = ComboBoxInTableWidget(fundConst.CATEGORY, value)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'to':
                comboBox = ComboBoxInTableWidget(fundConst.CATEGORY, value)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'associatedFund':
                comboBox = ComboBoxInTableWidget(fundConst.CATEGORY, value)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            else:
                print("未知的记录属性！！")
                return
        tableWidget.setCellWidget(current_row, len(keys_list), self.buttonsForExistRow(tableWidget))

    def setBlankTableCell(self, tableWidget, current_row, const_class):
        """
        Describe: 为表格的空白行设置单元格。根据列名设置对应类型(格式)的单元格

        Args:
            tableWidget: QTableWidget
                涉及的表格
            current_row: int
                本条记录所在行号
            const_class: Union[ExpenseConst, IncomeConst, MovementConst]
                记录类型对应的常量类
        """
        keys_list = [const_class.TABLEWIDGET_COLUMN_HEAD[tableWidget.horizontalHeaderItem(i).text()] for i in range(tableWidget.columnCount()-1)]
        for key in keys_list:
            if key == 'necessity':
                comboBox = ComboBoxInTableWidget(NECESSITY, 'True')
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'value':
                tableWidget.setItem(current_row, keys_list.index(key), QTableWidgetItem(''))
            elif key == 'category':
                comboBox = ComboBoxInTableWidget(const_class.CATEGORY, 0)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'detail':
                tableWidget.setItem(current_row, keys_list.index(key), QTableWidgetItem(''))
            elif key == 'describe':
                tableWidget.setItem(current_row, keys_list.index(key), QTableWidgetItem(' '))
            elif key == 'from':
                comboBox = ComboBoxInTableWidget(fundConst.CATEGORY, 0)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'to':
                comboBox = ComboBoxInTableWidget(fundConst.CATEGORY, 0)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            elif key == 'associatedFund':
                comboBox = ComboBoxInTableWidget(fundConst.CATEGORY, None)
                tableWidget.setCellWidget(current_row, keys_list.index(key), comboBox)
            else:
                print("未知的记录属性！！: {}", format(key))
                return
        tableWidget.setCellWidget(current_row, len(keys_list), self.buttonsForNewRow(tableWidget))

    def getExistTableCell(self, tableWidget, current_row, const_class):
        new_data_dict = OrderedDict()
        for i in range(tableWidget.columnCount() - 1):
            key = const_class.TABLEWIDGET_COLUMN_HEAD[tableWidget.horizontalHeaderItem(i).text()]
            if key == 'necessity':
                comboBox: ComboBoxInTableWidget = tableWidget.cellWidget(current_row, i)
                new_data_dict[key] = str(comboBox.getKeyByCurrentText())
            elif key == 'value':
                new_data_dict[key] = tableWidget.item(current_row, i).text()
            elif key == 'category':
                comboBox: ComboBoxInTableWidget = tableWidget.cellWidget(current_row, i)
                new_data_dict[key] = str(comboBox.getKeyByCurrentText())
            elif key == 'detail':
                new_data_dict[key] = tableWidget.item(current_row, i).text()
            elif key == 'describe':
                new_data_dict[key] = tableWidget.item(current_row, i).text()
            elif key == 'from':
                comboBox: ComboBoxInTableWidget = tableWidget.cellWidget(current_row, i)
                new_data_dict[key] = str(comboBox.getKeyByCurrentText())
            elif key == 'to':
                comboBox: ComboBoxInTableWidget = tableWidget.cellWidget(current_row, i)
                new_data_dict[key] = str(comboBox.getKeyByCurrentText())
            elif key == 'associatedFund':
                comboBox: ComboBoxInTableWidget = tableWidget.cellWidget(current_row, i)
                new_data_dict[key] = str(comboBox.getKeyByCurrentText())
            else:
                print("未知的记录属性！！: {}", format(key))
                return None
        return new_data_dict

    def updateExpenseTable(self, expenses_list):
        self.tableWidget_expense.setRowCount(0)
        self.tableWidget_expense.setRowCount(len(expenses_list)+1)

        current_row = 0
        for expense_dict in expenses_list:
            self.setExistTableCell(self.tableWidget_expense, current_row, expense_dict, expenseConst)
            current_row += 1

        self.setBlankTableCell(self.tableWidget_expense, current_row, expenseConst)

    def updateIncomeTable(self, incomes_list):
        self.tableWidget_income.setRowCount(0)
        self.tableWidget_income.setRowCount(len(incomes_list)+1)

        current_row = 0
        for income_dict in incomes_list:
            self.setExistTableCell(self.tableWidget_income, current_row, income_dict, incomeConst)
            current_row += 1

        self.setBlankTableCell(self.tableWidget_income, current_row, incomeConst)

    def updateMovementTable(self, movements_list):
        self.tableWidget_movement.setRowCount(0)
        self.tableWidget_movement.setRowCount(len(movements_list)+1)

        current_row = 0
        for movement_dict in movements_list:
            self.setExistTableCell(self.tableWidget_movement, current_row, movement_dict, movementConst)
            current_row += 1

        self.setBlankTableCell(self.tableWidget_movement, current_row, movementConst)

    def buttonsForExistRow(self, tableWidget):
        widget = QWidget()
        # 更新
        updateBtn = QPushButton('更新')
        updateBtn.clicked.connect(lambda: self.updateTableRow(updateBtn, tableWidget))
        # 删除
        deleteBtn = QPushButton('删除')
        deleteBtn.clicked.connect(lambda: self.deleteTableRow(deleteBtn, tableWidget))

        hLayout = QHBoxLayout(widget)
        hLayout.addWidget(updateBtn)
        hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        return widget

    def buttonsForNewRow(self, tableWidget):
        widget = QWidget()
        # 新增
        newBtn = QPushButton('新增')
        newBtn.clicked.connect(lambda: self.newTableRow(newBtn, tableWidget))

        hLayout = QHBoxLayout(widget)
        hLayout.addWidget(newBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        return widget

    def updateTableRow(self, triggeredBtn, tableWidget):
        pass

    def deleteTableRow(self, triggeredBtn, tableWidget):
        pass

    def newTableRow(self, triggeredBtn, tableWidget):
        print('触发了新增按钮')
        # 获取触发信号的控件所在行号
        current_row = tableWidget.indexAt(triggeredBtn.parent().pos()).row()
        if tableWidget == self.tableWidget_expense:
            const_class = expenseConst
        elif tableWidget == self.tableWidget_income:
            const_class = incomeConst
        elif tableWidget == self.tableWidget_movement:
            const_class = movementConst
        else:
            print('未知控件触发新增按钮！')
            return
        # 用新增行数据构建字典
        new_data_dict = self.getExistTableCell(tableWidget, current_row, const_class)
        if new_data_dict is None:
            print("获取新增数据失败！！")
            return
        print("新增记录内容为: \n", new_data_dict)

        # 插入新空行
        insert_pos = tableWidget.rowCount()
        tableWidget.insertRow(insert_pos)
        # 新空行初始化
        self.setBlankTableCell(tableWidget, insert_pos, const_class)
        # 新增行"操作"列转换按钮
        tableWidget.setCellWidget(insert_pos-1, tableWidget.columnCount()-1, self.buttonsForExistRow(tableWidget))

        # 用新增行的数据组织文件结构
        if tableWidget == self.tableWidget_expense:
            self.file_processor.organizeExpense(new_data_dict, self.dateEdit.text().replace('/', ''))
        elif tableWidget == self.tableWidget_income:
            self.file_processor.organizeIncome(new_data_dict, self.dateEdit.text().replace('/', ''))
        elif tableWidget == self.tableWidget_movement:
            self.file_processor.organizeMovement(new_data_dict, self.dateEdit.text().replace('/', ''))

        write_file_path = os.path.normpath(self.lineEdit_file_path.text())
        # print("输入框里的文件路径: ", write_file_path)
        self.file_processor.writeXMLFile(write_file_path)
