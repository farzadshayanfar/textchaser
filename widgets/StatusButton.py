from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton


class StatusButton(QPushButton):
    def __init__(self, label: str, icon: QPixmap, parent=None):
        QPushButton.__init__(self, parent=parent, icon=icon, text=label)
        self.setCheckable(True)
        self.setIconSize(QSize(20, 20))

        self.setAccessibleName("status_button")
