import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import MetaTrader5 as mt5

# подключимся к MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

pairs = [
    "EURUSDrfd",
    "GBPUSDrfd",
    "USDJPYrfd",
    "USDCHFrfd",
    "USDCADrfd",
    "AUDUSDrfd",
    "NZDUSDrfd",
    "USDRUBrfd",
    "EURRUBrfd",
    "EURJPYrfd",
    "EURCADrfd",
    "EURCHFrfd",
    "EURNZDrfd",
    "GBPCADrfd",
    "USDSGDrfd",
    "USDZARrfd",
    "EURDKKrfd",
    "EURNOKrfd",
    "EURSEKrfd",
    "GBPAUDrfd",
    "GBPCHFrfd",
    "GBPJPYrfd",
    "USDDKKrfd",
    "USDMXNrfd",
    "USDNOKrfd",
    "USDSEKrfd",
    "CHFJPYrfd",
    "GBPNZDrfd",
    "AUDCADrfd",
    "AUDCHFrfd",
    "AUDJPYrfd",
    "AUDNZDrfd",
    "EURAUDrfd",
    "EURGBPrfd",
]


def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]


O = 1
H = 2
L = 3
C = 4


def detect_reverse_bar(last_bar):
    price_open = last_bar[O]
    high = last_bar[H]
    low = last_bar[L]
    close = last_bar[C]

    part = (high - low) / 3

    bull_high = high
    bull_low = high - part
    bear_high = low + part
    bear_low = low

    if bear_high <= price_open <= bull_high and bull_low <= close <= bull_high:
        return 1
    elif bear_low <= price_open <= bull_low and bear_low <= close <= bear_high:
        return -1
    else:
        return 0
    pass


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.table = QtWidgets.QTableWidget(0, 8)

        for pair in pairs:
            pair = pair[:-3]
            row_1 = [insert_space(pair, 3), "", "", "", "", "", "", ""]
            self.addTableRow(row_1)

        hh = self.table.horizontalHeader()
        hh.setVisible(False)
        vh = self.table.verticalHeader()
        vh.setVisible(False)

        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 60)
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(3, 60)
        self.table.setColumnWidth(4, 60)
        self.table.setColumnWidth(5, 60)
        self.table.setColumnWidth(6, 60)
        self.table.setColumnWidth(7, 200)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.table)

        timer = QTimer(self)
        timer.timeout.connect(self.onTimeout)
        timer.start(2000)

    def onTimeout(self):
        for row_number in range(0, self.table.rowCount()):
            pair = self.table.item(row_number, 0).text()
            pair = pair.replace(" ", "") + "rfd"
            for timeframe in range(1, 7):
                item = self.table.item(row_number, timeframe)
                if timeframe == 1:
                    meta_frame = mt5.TIMEFRAME_M15
                    text = "M15"
                elif timeframe == 2:
                    meta_frame = mt5.TIMEFRAME_M30
                    text = "M30"
                elif timeframe == 3:
                    meta_frame = mt5.TIMEFRAME_H1
                    text = "H1"
                elif timeframe == 4:
                    meta_frame = mt5.TIMEFRAME_H4
                    text = "H4"
                elif timeframe == 5:
                    meta_frame = mt5.TIMEFRAME_D1
                    text = "D1"
                else:
                    meta_frame = mt5.TIMEFRAME_W1
                    text = "W1"
                detected = detect_reverse_bar(mt5.copy_rates_from_pos(pair, meta_frame, 0, 1)[0])

                if detected == 1:
                    item.setBackground(QtGui.QColor("green"))
                    item.setText(text)
                elif detected == -1:
                    item.setBackground(QtGui.QColor("red"))
                    item.setText(text)
                else:
                    item.setBackground(QtGui.QColor("white"))
                    item.setText("")



        # row_1 = ["1", "2", "3", "4", "", "6"]
        # self.addTableRow(row_1)
        # self.table.setRowHeight(0, 1)
        # print(type(self.table.item(0, 0).setBackground(QtGui.QColor("blue"))))
        pass

    def addTableRow(self, row_data):
        row = self.table.rowCount()
        self.table.setRowCount(self.table.rowCount() + 1)
        col = 0
        for item in row_data:
            cell = QtWidgets.QTableWidgetItem(str(item))
            self.table.setItem(row, col, cell)
            col += 1
        self.table.setRowHeight(row, 1)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.setWindowTitle("Reverse Bars With Alligator Filter")
    widget.resize(645, 845)
    widget.show()
    sys.exit(app.exec())
