import sys
from PyQt5.QtWidgets import QApplication

from window import Window


def application():
    app = QApplication(sys.argv)
    m = Window()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
