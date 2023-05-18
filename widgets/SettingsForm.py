from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSplitter, QVBoxLayout, QHBoxLayout
from widgets import MainForm
from settings import Settings


class SettingsForm(QWidget):
    Title: str = "Settings"
    MinimumWidth: int = 300
    MinimumHeight: int = 400

    def __init__(self, parent: MainForm, settings: Settings):
        super(SettingsForm, self).__init__(parent=parent)
        self._mainFormHandle: MainForm = parent
        self._settings: Settings = settings

        self.setWindowTitle(self.Title)
        self.setMinimumSize(self.MinimumWidth, self.MinimumHeight)
        self.resize(self.MinimumWidth + 50, self.MinimumHeight + 50)
        self._mainLayout = QVBoxLayout()
        self.setLayout(self._mainLayout)
        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._bottomLayout = QHBoxLayout()
        self._mainLayout.addWidget(self._splitter)
        self._mainLayout.addLayout(self._bottomLayout)

