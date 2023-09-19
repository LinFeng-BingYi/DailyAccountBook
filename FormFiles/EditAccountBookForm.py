from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QTableWidgetItem
from PySide6.QtCore import Qt, QDate

import os

from FormFiles.EditAccountBook import Ui_EditAccountBook
from FileProcess.AccountBookXML import AccountBookXMLProcessor

TABLEWIDGET_EXPENSE_COLUMN_HEAD = {'基本需求': 'necessity', '数值': 'value', '类别': 'category', '细则': 'detail', '描述': 'describe', '支出账户': 'from', '关联账户': 'associatedFund', '操作': ''}
TABLEWIDGET_INCOME_COLUMN_HEAD = {'数值': 'value', '类别': 'category', '细则': 'detail', '描述': 'describe', '收入账户': 'to', '关联账户': 'associatedFund', '操作': ''}
TABLEWIDGET_MOVEMENT_COLUMN_HEAD = {'数值': 'value', '细则': 'detail', '描述': 'describe', '转出账户': 'from', '转入账户': 'to', '操作': ''}


class WidgetEditAccountBook(QWidget, Ui_EditAccountBook):

    def __init__(self):
        super(WidgetEditAccountBook, self).__init__()
        self.setupUi(self)
        self.tableWidget_expense.setColumnCount(len(TABLEWIDGET_EXPENSE_COLUMN_HEAD))
        self.tableWidget_expense.setHorizontalHeaderLabels(list(TABLEWIDGET_EXPENSE_COLUMN_HEAD))
        self.tableWidget_income.setColumnCount(len(TABLEWIDGET_INCOME_COLUMN_HEAD))
        self.tableWidget_income.setHorizontalHeaderLabels(list(TABLEWIDGET_INCOME_COLUMN_HEAD))
        self.tableWidget_movement.setColumnCount(len(TABLEWIDGET_MOVEMENT_COLUMN_HEAD))
        self.tableWidget_movement.setHorizontalHeaderLabels(list(TABLEWIDGET_MOVEMENT_COLUMN_HEAD))

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

    def updateExpenseTable(self, expenses_list):
        self.tableWidget_expense.setRowCount(0)
        self.tableWidget_expense.setRowCount(len(expenses_list)+1)

        current_row = 0
        for expense_dict in expenses_list:
            self.tableWidget_expense.setItem(current_row, 0, QTableWidgetItem(str(expense_dict['necessity'])))
            self.tableWidget_expense.setItem(current_row, 1, QTableWidgetItem(str(expense_dict['value'])))
            self.tableWidget_expense.setItem(current_row, 2, QTableWidgetItem(str(expense_dict['category'])))
            self.tableWidget_expense.setItem(current_row, 3, QTableWidgetItem(str(expense_dict['detail'])))
            self.tableWidget_expense.setItem(current_row, 4, QTableWidgetItem(str(expense_dict['describe'])))
            self.tableWidget_expense.setItem(current_row, 5, QTableWidgetItem(str(expense_dict['from'])))
            self.tableWidget_expense.setItem(current_row, 6, QTableWidgetItem(str(expense_dict['associatedFund'])))
            self.tableWidget_expense.setCellWidget(current_row, 7, self.buttonsForExistRow(self.tableWidget_expense))
            current_row += 1

        self.tableWidget_expense.setItem(current_row, 4, QTableWidgetItem(' '))
        self.tableWidget_expense.setCellWidget(current_row, 7, self.buttonsForNewRow(self.tableWidget_expense))

    def updateIncomeTable(self, incomes_list):
        self.tableWidget_income.setRowCount(0)
        self.tableWidget_income.setRowCount(len(incomes_list)+1)

        current_row = 0
        for income_dict in incomes_list:
            self.tableWidget_income.setItem(current_row, 0, QTableWidgetItem(str(income_dict['value'])))
            self.tableWidget_income.setItem(current_row, 1, QTableWidgetItem(str(income_dict['category'])))
            self.tableWidget_income.setItem(current_row, 2, QTableWidgetItem(str(income_dict['detail'])))
            self.tableWidget_income.setItem(current_row, 3, QTableWidgetItem(str(income_dict['describe'])))
            self.tableWidget_income.setItem(current_row, 4, QTableWidgetItem(str(income_dict['to'])))
            self.tableWidget_income.setItem(current_row, 5, QTableWidgetItem(str(income_dict['associatedFund'])))
            self.tableWidget_income.setCellWidget(current_row, 6, self.buttonsForExistRow(self.tableWidget_income))
            current_row += 1

        self.tableWidget_income.setItem(current_row, 3, QTableWidgetItem(' '))
        self.tableWidget_income.setCellWidget(current_row, 6, self.buttonsForNewRow(self.tableWidget_income))

    def updateMovementTable(self, movements_list):
        self.tableWidget_movement.setRowCount(0)
        self.tableWidget_movement.setRowCount(len(movements_list)+1)

        current_row = 0
        for movement_dict in movements_list:
            self.tableWidget_movement.setItem(current_row, 0, QTableWidgetItem(str(movement_dict['value'])))
            self.tableWidget_movement.setItem(current_row, 1, QTableWidgetItem(str(movement_dict['detail'])))
            self.tableWidget_movement.setItem(current_row, 2, QTableWidgetItem(str(movement_dict['describe'])))
            self.tableWidget_movement.setItem(current_row, 3, QTableWidgetItem(str(movement_dict['from'])))
            self.tableWidget_movement.setItem(current_row, 4, QTableWidgetItem(str(movement_dict['to'])))
            self.tableWidget_movement.setCellWidget(current_row, 5, self.buttonsForExistRow(self.tableWidget_movement))
            current_row += 1

        self.tableWidget_movement.setItem(current_row, 2, QTableWidgetItem(' '))
        self.tableWidget_movement.setCellWidget(current_row, 5, self.buttonsForNewRow(self.tableWidget_movement))

    def buttonsForExistRow(self, tableWidget):
        widget = QWidget()
        # 更新
        updateBtn = QPushButton('更新')
        updateBtn.clicked.connect(lambda: self.updateTableRow(tableWidget))
        # 删除
        deleteBtn = QPushButton('删除')
        deleteBtn.clicked.connect(lambda: self.deleteTableRow(tableWidget))

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

    def updateTableRow(self, toggledBtn, tableWidget):
        pass

    def deleteTableRow(self, toggledBtn, tableWidget):
        pass

    def newTableRow(self, toggledBtn, tableWidget):
        print('触发了新增按钮')
        # 获取触发信号的控件所在行号
        row = tableWidget.indexAt(toggledBtn.parent().pos()).row()
        new_data_dict = dict()
        if tableWidget == self.tableWidget_expense:
            current_column_head = TABLEWIDGET_EXPENSE_COLUMN_HEAD
        elif tableWidget == self.tableWidget_income:
            current_column_head = TABLEWIDGET_INCOME_COLUMN_HEAD
        elif tableWidget == self.tableWidget_movement:
            current_column_head = TABLEWIDGET_MOVEMENT_COLUMN_HEAD
        else:
            print('未知控件触发新增按钮！')
            return
        # 用新增行数据构建字典
        for i in range(tableWidget.columnCount()-1):
            new_data_dict[current_column_head[tableWidget.horizontalHeaderItem(i).text()]] = tableWidget.item(row, i).text()
        print(new_data_dict)

        # 插入新空行
        insert_pos = tableWidget.rowCount()
        tableWidget.insertRow(insert_pos)
        # 新空行"操作"列初始化按钮
        tableWidget.setCellWidget(insert_pos, tableWidget.columnCount()-1, self.buttonsForNewRow(tableWidget))
        # 新增行"操作"列初始化按钮
        tableWidget.setCellWidget(insert_pos-1, tableWidget.columnCount()-1, self.buttonsForExistRow(tableWidget))

        if tableWidget == self.tableWidget_expense:
            # 将"描述"字段预置空格
            tableWidget.setItem(insert_pos, 4, QTableWidgetItem(' '))
            # 用新增行的数据组织文件结构
            self.file_processor.organizeExpense(new_data_dict, self.dateEdit.text().replace('/', ''))
        elif tableWidget == self.tableWidget_income:
            tableWidget.setItem(insert_pos, 3, QTableWidgetItem(' '))
            self.file_processor.organizeIncome(new_data_dict, self.dateEdit.text().replace('/', ''))
        elif tableWidget == self.tableWidget_movement:
            tableWidget.setItem(insert_pos, 2, QTableWidgetItem(' '))
            self.file_processor.organizeMovement(new_data_dict, self.dateEdit.text().replace('/', ''))

        self.file_processor.writeXMLFile(self.cwd+'\\AccountBookXMLFile.xml')
