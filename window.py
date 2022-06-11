# window.py
import time

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QMainWindow
from PyQt5.QtCore import Qt

from menu import Menu
from game import Game
from info import Info
from settings import Settings


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(640, 490)

        self.btn_back_to_menu = QPushButton(Form)
        self.btn_back_to_menu.setObjectName("WindowButton")
        self.btn_back_to_menu.resize(100, 20)
        self.btn_back_to_menu.move(10, 10)

        self.info = Info(Form.ai_settings, width=150, height=150, x=Form.width(), y=0, parent=Form)
        self.info.setStyleSheet(" background-color: gray; ")
        self.info.move(-100, -100)

        self.game = Game(Form.ai_settings, self.info, width=315, height=315, x=130, y=95, parent=Form)
        self.game.setStyleSheet(" background-color: red; ")
        self.game.move(-100, -100)

        self.menu = Menu(Form.ai_settings, width=355, height=175, x=130, y=200, parent=Form)
        self.menu.setStyleSheet(" background-color: green; ")
        self.menu.move(-100, -100)

        with open("style.txt", 'r') as f:
            style = f.read()
            Form.setStyleSheet(style)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Assemble chain"))
        self.btn_back_to_menu.setText(_translate("Form", "BACK TO MENU"))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai_settings = Settings()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.menu.show()
        self.ui.btn_back_to_menu.clicked.connect(self.event_back_to_menu)
        # self.ui.music.clicked.connect(self.event_music)

    def event_back_to_menu(self):
        """ Вернуться в меню (открыть) """
        self.ui.menu.widget.show()
        self.ai_settings.flag = False

    def keyPressEvent(self, e):
        """ keyboard events """

        # Closes the window when you click on the escape button
        if e.key() == Qt.Key_Escape:
            self.close()
