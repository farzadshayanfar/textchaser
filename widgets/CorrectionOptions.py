from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout


class CorrectionOptions(QDialog):
    Auto = 0

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ImageViewArea = parent
        self.setWindowTitle("Correction Options")
        self.setWindowIcon(QIcon("res/icons/correction.png"))
        self.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(250, 200)

        self.okBtn = QPushButton("Okay")

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.okBtn, alignment=Qt.AlignHCenter)

        self.okBtn.clicked.connect(lambda: self.setVisible(False))
