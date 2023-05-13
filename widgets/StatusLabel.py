from PySide6.QtWidgets import QLabel


class StatusLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setAccessibleName("StatusLabel")
