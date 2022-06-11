# menu.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel


class Menu(QWidget):
    def __init__(self, settings, parent=None, width=355, height=175, x=0, y=0):
        """ Initialize the window and display its contents to the screen Menu """
        super().__init__(parent)
        self.parent = parent
        self.ai_settings = settings

        self.widget = QWidget(parent)
        self.widget.setAttribute(Qt.WA_NoSystemBackground, True)
        self.widget.setFixedSize(width, height)
        self.widget.move(x, y)

        self.v_btn_box = QVBoxLayout(self.widget)
        self.title = QLabel("Chain Factor")
        self.title.setObjectName("MenuLabel")

        self.btn_play = QPushButton('Play')
        self.btn_play.setObjectName("MenuButton")
        self.btn_play.clicked.connect(self.event_btn_play)

        self.btn_delete_score = QPushButton("delete Score")
        self.btn_delete_score.setObjectName("MenuButton")
        self.btn_delete_score.clicked.connect(self.event_btn_delete_score)

        self.v_btn_box.addWidget(self.title)
        self.v_btn_box.addWidget(self.btn_play)
        self.v_btn_box.addWidget(self.btn_delete_score)

        with open("style.txt", 'r') as f:
            style = f.read()
            self.widget.setStyleSheet(style)
        self.show()

    def event_btn_play(self):
        self.widget.hide()
        self.ai_settings.flag = True

    def event_btn_delete_score(self):
        with open('cookie.txt', 'w') as cookie:
            cookie.write('high score: 0')
