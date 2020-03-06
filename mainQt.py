import sys
from PySide2.QtCore import Qt
from PySide2.QtGui import (QPainter, QBrush, QPen)
from PySide2.QtWidgets import (QApplication, QMainWindow, )

class ZWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Z - Interactive Graphic System"
        self.top = 150
        self.left = 150
        self.width = 500
        self.height = 500
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,  4, Qt.SolidLine))
        painter.drawLine(50,50, 100, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    igs = ZWindow()
    sys.exit(app.exec_())
