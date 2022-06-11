# game.py

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from progress_game import ProgressGame
from tableGame import TableGame


class Game(QWidget):
    def __init__(self, settings, infoGame, parent=None, width=315, height=315, x=0, y=0):
        super().__init__(parent)
        self.parent = parent
        self.ai_settings = settings
        self.info_game = infoGame
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y
        self.initializeUI()

    def initializeUI(self):
        """ display window game """
        self.progress = ProgressGame(self.ai_settings)

        self.tableGame = TableGame(self.ai_settings, self.info_game, self.progress, sizeRow=45, sizeCol=45, parent=self.parent)
        self.tableGame.resize(self.__width, self.__height)
        self.tableGame.move(self.__x, self.__y)

        self.under_table = QWidget(self.parent)
        self.under_table.setFixedWidth(self.__width)
        self.under_table.setFixedHeight(50)
        self.under_table.move(self.__x, self.__y + self.tableGame.height())

        vbox = QVBoxLayout()
        vbox.addWidget(self.progress)

        self.under_table.setLayout(vbox)

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(0.5)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())
