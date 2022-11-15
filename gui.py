from PyQt5.QtCore import Qt, QTime, QDateTime
from PyQt5.QtWidgets import QTableWidgetItem
from db import Database
import sys

from PyQt5 import QtWidgets
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("forms/main.ui", self)

        self.db = Database()

        self.ui.add_dep.clicked.connect(self.new_deposit)  # Кнопки взаимодействия с таблицей "Диски"
        self.ui.delete_dep.clicked.connect(self.delete_deposit)
        self.ui.save_dep.clicked.connect(self.save_deposit)

        self.ui.emp_add.clicked.connect(self.new_employee)  # Кнопки взаимодействия с таблицей "Должники"
        self.ui.emp_delete.clicked.connect(self.delete_employee)
        self.ui.emp_save.clicked.connect(self.save_employee)

        self.updateTableCDs()
        self.updateTableDebtors()

#######################################################
    def updateTableCDs(self):
        self.table_currencies.clear()
        rec = self.db.selectCDs()
        self.ui.table_cds.setColumnCount(5)
        self.ui.table_cds.setRowCount(len(rec))
        self.ui.table_cds.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Описание', 'Жанр','Издатель'])

        for i, exposition in enumerate(rec):
            for x, field in enumerate(exposition):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_currencies.setItem(i, x, item)

    def updateTableDebtors(self):
        self.table_employees.clear()
        rec = self.db.selectDebtors()
        self.ui.table_debtors.setColumnCount(4)
        self.ui.table_debtors.setRowCount(len(rec))
        self.ui.table_debtors.setHorizontalHeaderLabels(
            ['ID', 'Имя должника', 'Дата', 'Код Диска'])

        for i, exposition in enumerate(rec):
            for x, field in enumerate(exposition):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_employees.setItem(i, x, item)

    def getFromTableСDs(self):
        rows = self.table_cds.rowCount()
        cols = self.table_cds.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_cds.item(row, col).text())
            data.append(tmp)
        return data

    def getFromTableDebtors(self):
        rows = self.table_debtors.rowCount()
        cols = self.table_debtors.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_debtors.item(row, col).text())
            data.append(tmp)
        return data

    def new_cd(self):
        curr_name = self.ui.curr_name.text()
        curr_ex_rate = float(self.ui.curr_ex_rate.text())

        self.db.insertCDs(curr_name, curr_ex_rate)
        self.updateTableCDs()

    def new_debtor(self):
        dep_name = self.ui.dep_name_line.text()
        percent_rate = float(self.ui.percent_line.text())
        curr_id = int(self.ui.id_curr_line.text())
        depositor_id = int(self.ui.id_depositor_line.text())

        self.db.insertDebtors(dep_name, percent_rate, curr_id, depositor_id)
        self.updateTableDeposits()

    def delete_currency(self):
        SelectedRow = self.table_currencies.currentRow()
        rowcount = self.table_currencies.rowCount()
        colcount = self.table_currencies.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_currencies.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_currencies.model().index(-1, -1)
            self.table_currencies.setCurrentIndex(ix)

    def delete_deposit(self):
        SelectedRow = self.table_deposit.currentRow()
        rowcount = self.table_deposit.rowCount()
        colcount = self.table_deposit.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_deposit.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_deposit.model().index(-1, -1)
            self.table_deposit.setCurrentIndex(ix)

    def save_currency(self):
        data = self.getFromTableCurrencies()
        for string in data:
            if string[1] != '':
                self.db.updateCurrencies(int(string[0]), string[1], float(string[2]))
            else:
                self.db.deleteCurrencies(int(string[0]))
        self.updateTableCurrencies()

    def delete_depositors(self):
        SelectedRow = self.table_depositors.currentRow()
        rowcount = self.table_depositors.rowCount()
        colcount = self.table_depositors.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_depositors.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_depositors.model().index(-1, -1)
            self.table_depositors.setCurrentIndex(ix)

    def save_deposit(self):
        data = self.getFromTableDeposits()
        for string in data:
            if string[1] != '':
                self.db.updateDeposits(int(string[0]), string[1], float(string[2]), int(string[3]), int(string[4]))
            else:
                self.db.deleteDeposits(int(string[0]))
        self.updateTableDeposits()

    def save_employee(self):
        data = self.getFromTableEmployees()
        for string in data:
            if string[1] != '':
                self.db.updateEmployees(int(string[0]), string[1], string[2], string[3], string[4], string[5], string[6], int(string[7]))
            else:
                self.db.deleteEmployees(int(string[0]))
        self.updateTableEmployees()

    def save_position(self):
        data = self.getFromTablePositions()
        for string in data:
            if string[1] != '':
                self.db.updatePositions(int(string[0]), string[1], int(string[2]), string[3], string[4])
            else:
                self.db.deletePositions(int(string[0]))
        self.updateTablePositions()

    def save_depositors(self):
        data = self.getFromTableDepositors()
        for string in data:
            if string[1] != '':
                self.db.updateDepositors(int(string[0]), string[1], string[2], string[3], int(string[4]), int(string[5]), string[6], string[7], string[8], int(string[9]))
            else:
                self.db.deleteDepositors(int(string[0]))
        self.updateTableDepositors()

    def mes_box(self, text):
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()


class Builder:
    def __init__(self):
        self.qapp = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        self.qapp.exec()


if __name__ == '__main__':
    B = Builder()
