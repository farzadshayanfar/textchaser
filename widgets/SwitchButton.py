from PySide6 import QtGui
from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QPushButton


class SwitchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        # self.setMinimumWidth(160)
        # self.setMinimumHeight(50)
        self.setFixedSize(85, 38)

        self.setStyleSheet("""
        font-size: 10pt;
        font-style: italic;
        """)

    def paintEvent(self, event):
        label = "Scene     " if self.isChecked() else "       Docs"
        bg_color = QtGui.QColor(176, 174, 172)

        radius = 13
        width = 80
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(235, 235, 235))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(0)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2 * radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
