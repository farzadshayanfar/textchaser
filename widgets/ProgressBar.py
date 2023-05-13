from PySide6.QtGui import Qt
from PySide6.QtWidgets import QProgressBar, QSizePolicy


class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        QProgressBar.__init__(self, parent)
        self.setRange(0, 100)
        self.setValue(0)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignCenter)

    def getStep(self, items_count):
        remainder = 100 - self.value()
        step = round(remainder / items_count, 2)
        return step

    def advance(self, int, finished=0):
        if finished:
            self.setValue(100)
            self.setVisible(False)
            self.reset()
            return
        self.setValue(self.value() + int)
