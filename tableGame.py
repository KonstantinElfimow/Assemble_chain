# tableGame.py
import random

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem

import game_function as gf


class TableGame(QTableWidget):
    cellExited = QtCore.pyqtSignal(int, int)
    itemExited = QtCore.pyqtSignal(QTableWidgetItem)

    def __init__(self, settings=None, infoGame=None, progress=None, sizeRow=10, sizeCol=10, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ai_settings = settings
        self.info_game = infoGame
        self.progress = progress
        self.__sizeRow = sizeRow
        self.__sizeCol = sizeCol

        self._last_index = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)

        # random number (icon)
        self.list_link_icon_str = ['gray_whole', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'gray_broken', ]
        self.list_link_icon_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, ]
        self.head_icon = random.randint(0, len(self.list_link_icon_str) - 2)

        self.data = []

        # Создание таблицы и ее интерфейса
        self.setupUI()

    def setupUI(self):
        """ Создает таблицу с отображением контактов """

        self.setMouseTracking(True)
        self.itemEntered.connect(self.handleItemEntered)
        self.itemExited.connect(self.handleItemExited)

        self.setRowCount(7)
        self.setColumnCount(7)

        # Убирает вертикальный заголовок
        self.verticalHeader().setVisible(False)

        # Убирает горизонтальный заголовок
        self.horizontalHeader().setVisible(False)

        # Удаляет вертикальную полосу прокрутки
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Удаляет горизонтальную полосу прокрутки
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Запрещает выделять ячейки
        self.setSelectionMode(QAbstractItemView.NoSelection)

        # Запрещает изменять содержимое ячейки
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setIconSize(QSize(45, 45))

        for row in range(self.rowCount()):
            # Заполнение data (представление таблицы в двумерном массиве)
            self.data.append(['' for _ in range(self.columnCount())])
            self.setRowHeight(row, self.__sizeRow)
            for column in range(self.columnCount()):
                self.setColumnWidth(column, self.__sizeCol)

                item = QTableWidgetItem('')
                self.setItem(row, column, item)

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QtCore.QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QtCore.QEvent.Leave:
                index = QtCore.QModelIndex()
            if index != self._last_index:
                row = self._last_index.row()
                column = self._last_index.column()
                item = self.item(row, column)
                if item is not None:
                    self.itemExited.emit(item)
                self.cellExited.emit(row, column)
                self._last_index = QtCore.QPersistentModelIndex(index)
        return QTableWidget.eventFilter(self, widget, event)

    def handleItemEntered(self, item):
        """ Наведение мыши показывает иконку на верхушке столбца """
        if self.ai_settings.flag:
            self.item(0, item.column()).setIcon(QIcon(f"img/{self.list_link_icon_str[self.head_icon]}.png"))

    def handleItemExited(self, item):
        """ Отведение мыши с прошлой наведенной столбца """
        if self.ai_settings.flag:
            self.item(0, item.column()).setIcon(QIcon())

    def mouseReleaseEvent(self, e):
        """ Обработка события отпуская кнопки мыши """
        if self.ai_settings.flag:
            QTableWidget.mouseReleaseEvent(self, e)  # в начале правильная обработка
            if e.button() == Qt.LeftButton:
                gf.update_screen(self, self.ai_settings, self.progress)
                self.progress.update()
                self.info_game.update()

    def draw_table(self):
        """ Отрисовка таблицы по данным data """
        for row in range(len(self.data)):
            for column in range(len(self.data[0])):
                if self.data[row][column] == '':
                    self.item(row, column).setIcon(QIcon(f"img/pass.png"))
                    continue
                self.item(row, column).setIcon(QIcon(f"img/{self.list_link_icon_str[self.data[row][column]]}.png"))
