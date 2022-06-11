# progress_game.py

from PyQt5.QtWidgets import QWidget, QLabel


class ProgressGame(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.ai_settings = settings

        self.number_destroyed = -1

        self.label_num_level = QLabel(f'LEVEL {self.ai_settings.lvl}', self)

        self.progressBar = [QLabel('', self) for _ in range(self.ai_settings.step_to_next_lvl)]

        self.update()

    def update(self):
        self.number_destroyed += 1

        for i in range(self.ai_settings.step_to_next_lvl):
            label = self.progressBar[i]
            label.move(i * 10, 20)
            label.resize(8, 8)
            if i < self.number_destroyed:
                label.setStyleSheet("""
                            border-radius: 4px;
                            background-color: black;
                            """)
            else:
                label.setStyleSheet("""
                            border-radius: 4px;
                            background-color: rgb(191, 191, 191);
                            """)
