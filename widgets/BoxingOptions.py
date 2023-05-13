from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel, QSpinBox, QComboBox, QPushButton, QGridLayout, QCheckBox


class BoxingOptions(QDialog):
    Left2Right = "left to right"
    Right2Left = "right to left"
    Top2Bottom = "top to bottom"
    Bottom2Top = "bottom to top"

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.mainFormHandle = parent

        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowTitle("Boxing Options")
        self.setWindowIcon(QIcon("res/icons/boxingOptions.png"))
        self.setFixedSize(280, 190)

        self.boxPaddingLabel = QLabel("Padding:")
        self.boxPaddingLabel.setWordWrap(True)
        self.boxPaddingInput = QSpinBox()
        self.boxPaddingInput.setRange(0, 40)
        self.boxPaddingInput.setValue(self.mainFormHandle.paddingValue)
        self.boxPaddingInput.setWhatsThis("""<p style="text-align: justify;">the <strong>padding value</strong> 
        is the value to be added&nbsp;to the extracted boxes by the engine.&nbsp;this value helps to increase chance of
        inclusion for&nbsp;the bounded area within the extracted box.</p>""")

        self.boxingDirectionLbl = QLabel("Select the boxing direction:")
        self.boxingDirectionLbl.setWordWrap(True)
        self.boxingDirectionCombo = QComboBox()
        self.boxingDirectionCombo.addItems((self.Left2Right, self.Right2Left, self.Top2Bottom, self.Bottom2Top))
        for idx in range(0, 4):
            if self.boxingDirectionCombo.itemText(idx) == self.mainFormHandle.boxingDirection:
                self.boxingDirectionCombo.setCurrentIndex(idx)
                break
        self.boxingDirectionCombo.setEditable(False)

        self.showWordBoxingChk = QCheckBox(text="Show word boxings")
        self.showWordBoxingChk.setChecked(True) if self.mainFormHandle.showWordBoxing else \
            self.showWordBoxingChk.setChecked(False)

        self.okBtn = QPushButton("Okay")

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.boxPaddingLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.boxPaddingInput, 0, 2, 1, 1)
        self.layout.addWidget(self.boxingDirectionLbl, 1, 0, 1, 2)
        self.layout.addWidget(self.boxingDirectionCombo, 1, 2, 1, 1)
        self.layout.addWidget(self.showWordBoxingChk, 2, 1, 1, 2)
        self.layout.addWidget(self.okBtn, 3, 2, 1, 1, alignment=Qt.AlignHCenter)

        self.okBtn.clicked.connect(self.applyChanges)

    def applyChanges(self):
        self.mainFormHandle.boxingDirection = self.boxingDirectionCombo.currentText()
        self.mainFormHandle.paddingValue = self.boxPaddingInput.value()
        if self.showWordBoxingChk.isChecked():
            self.mainFormHandle.showWordBoxing = True
        else:
            self.mainFormHandle.showWordBoxing = False

        self.close()
