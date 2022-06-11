# info.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Info(QWidget):
    def __init__(self, settings, parent=None, width=150, height=150, x=0, y=0):
        """ display window info """
        super().__init__(parent)
        self.parent = parent
        self.ai_settings = settings

        self.widget = QWidget(parent)
        self.widget.setAttribute(Qt.WA_NoSystemBackground, True)
        self.widget.setFixedSize(width, height)
        self.widget.move(x - width, y)

        vbox = QVBoxLayout(self.widget)
        self.score = QLabel('0')
        self.score.setObjectName("InfoLabel")

        self.longest_chain = QLabel(f'LONGEST CHAIN: {self.ai_settings.longest_chain}')
        self.longest_chain.setObjectName("InfoLabelAdd")

        self.high_score = QLabel(f'HIGH SCORE\n{0}')
        self.high_score.setObjectName("InfoLabelAdd")

        vbox.addWidget(self.score)
        vbox.addWidget(self.longest_chain)
        vbox.addWidget(self.high_score)

        with open("style.txt", 'r') as f:
            style = f.read()
            self.widget.setStyleSheet(style)
        self.show()

    def update(self):
        self.score.setText(f'{self.ai_settings.score}')
        self.longest_chain.setText(f'LONGEST CHAIN: {self.ai_settings.longest_chain}')
        self.high_score.setText(f'HIGH SCORE\n{self.ai_settings.high_score}')
