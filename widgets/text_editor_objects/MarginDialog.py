from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QDialog, QLabel, QSpinBox, QPushButton, QFormLayout


class MarginDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.Editor = parent

        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowTitle("Doc Margin")
        self.setWindowIcon(QIcon("res/icons/margin.png"))
        self.setFixedSize(230, 100)

        self.marginLabel = QLabel("Margin:")
        self.marginLabel.setFixedWidth(90)
        self.marginSpin = QSpinBox()
        self.marginSpin.setFixedWidth(90)
        self.marginSpin.setRange(0, 60)
        self.marginSpin.setValue(self.Editor.docMargin)

        self.okBtn = QPushButton("Okay")
        self.okBtn.clicked.connect(self.setMargins)
        self.okBtn.setFixedWidth(90)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.close)
        self.cancelBtn.setFixedWidth(90)

        self.layout = QFormLayout(self)
        self.layout.addRow(self.marginLabel, self.marginSpin)
        self.layout.addRow(self.cancelBtn, self.okBtn)

    def setMargins(self):
        self.Editor.docMargin = self.marginSpin.value()
        self.Editor.text.document().setDocumentMargin(self.Editor.docMargin)
        self.close()
