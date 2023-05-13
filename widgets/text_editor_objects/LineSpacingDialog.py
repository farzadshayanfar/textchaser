from PySide6.QtGui import QIcon, QTextBlockFormat, Qt
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QFormLayout, QDoubleSpinBox


class LineSpacingDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.Editor = parent

        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowTitle("Line Height")
        self.setWindowIcon(QIcon("res/icons/spacing.png"))
        self.setFixedSize(230, 100)

        self.spacingLabel = QLabel("Line height:")
        self.spacingLabel.setFixedWidth(90)
        self.spacingSpin = QDoubleSpinBox()
        self.spacingSpin.setDecimals(1)
        self.spacingSpin.setFixedWidth(90)
        self.spacingSpin.setRange(0, 100)
        self.spacingSpin.setValue(self.Editor.lineSpacing)

        self.okBtn = QPushButton("Okay")
        self.okBtn.clicked.connect(self.setMargins)
        self.okBtn.setFixedWidth(90)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.close)
        self.cancelBtn.setFixedWidth(90)

        self.layout = QFormLayout(self)
        self.layout.addRow(self.spacingLabel, self.spacingSpin)
        self.layout.addRow(self.cancelBtn, self.okBtn)

    def setMargins(self):
        self.Editor.lineSpacing = self.spacingSpin.value()
        block_format = QTextBlockFormat()
        block_format.setLineHeight(self.Editor.lineSpacing, QTextBlockFormat.LineDistanceHeight)
        self.Editor.text.textCursor().setBlockFormat(block_format)
        self.close()
