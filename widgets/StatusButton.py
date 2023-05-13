from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton


class StatusButton(QPushButton):
    def __init__(self, label, parent=None):
        QPushButton.__init__(self, parent=None)
        self.setText(label)
        self.setFixedSize(85, 38)
        self.setCheckable(True)
        self.setIconSize(QSize(25, 25))

        self.setAccessibleName("StatusButton")
