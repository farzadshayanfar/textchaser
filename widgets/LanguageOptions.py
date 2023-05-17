from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QListWidget, QListWidgetItem, QMessageBox

from .tesseract_langs import langs


class LanguageOptions(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.mainFormHandle = parent

        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowTitle("Language Options")
        self.setWindowIcon(QIcon("res/icons/lang2.png"))
        self.setFixedSize(380, 450)

        self.langLabel = QLabel("Add language(s) for text extraction:")
        self.langLabel.setWordWrap(True)

        self.langCombo = QComboBox()
        self.langCombo.addItems(langs)
        self.langCombo.setCurrentIndex(self.mainFormHandle.extractionLangIndex)

        self.addLangBtn = QPushButton()
        self.addLangBtn.setToolTip("Add the current language to the list")
        self.addLangBtn.setIcon(QIcon("res/icons/more.svg"))
        self.addLangBtn.setFixedWidth(50)
        self.addLangBtn.clicked.connect(self.addLangClickedFcn)

        self.anHLayout1 = QHBoxLayout()
        self.anHLayout1.addWidget(self.langCombo)
        self.anHLayout1.addWidget(self.addLangBtn)

        self.addedLangsList = list()
        self.addedLangsList = self.mainFormHandle.selectedLangsList
        self.addedLangsString = str()
        self.addedLangsLabel = QLabel()
        self.addedLangsLabel.setStyleSheet("color: #35788f;")

        if len(self.mainFormHandle.selectedLangsList) > 0:
            self.displayLangs()
        else:
            self.addedLangsList.append("eng (English)")
            self.addedLangsLabel.setText("Selected Language(s): " + "eng")

        self.addedLangsListWidget = QListWidget()
        self.addedLangsListWidget.addItems(self.addedLangsList)

        self.moveUpBtn = QPushButton()
        self.moveUpBtn.setToolTip("Move the selected language up")
        self.moveUpBtn.setIcon(QIcon("res/icons/moveup.svg"))
        self.moveUpBtn.setFixedWidth(40)
        self.moveUpBtn.clicked.connect(self.moveUp)

        self.moveDownBtn = QPushButton()
        self.moveDownBtn.setToolTip("Move the selected language down")
        self.moveDownBtn.setIcon(QIcon("res/icons/movedown.svg"))
        self.moveDownBtn.setFixedWidth(40)
        self.moveDownBtn.clicked.connect(self.moveDown)

        self.removeBtn = QPushButton()
        self.removeBtn.setToolTip("Remove the selected language from the list")
        self.removeBtn.setIcon(QIcon("res/icons/cross.svg"))
        self.removeBtn.setFixedWidth(40)
        self.removeBtn.clicked.connect(self.removeSelectedLang)

        self.anHLayout2 = QHBoxLayout()
        self.anHLayout2.setSpacing(10)
        self.anHLayout2.insertStretch(0, 1)
        self.anHLayout2.addWidget(self.moveUpBtn)
        self.anHLayout2.addWidget(self.moveDownBtn)
        self.anHLayout2.addWidget(self.removeBtn)

        self.segLabel = QLabel("Select segmentation mode:")
        self.segCombo = QComboBox()
        seg_modes = ["Orientation and script detection (OSD) only",
                     "Automatic page segmentation with OSD",
                     "Automatic page segmentation, but no OSD, or OCR",
                     "Fully automatic page segmentation, but no OSD (default)",
                     "Assume a single column of text of variable sizes",
                     "Assume a single uniform block of vertically aligned text",
                     "Assume a single uniform block of text",
                     "Treat the image as a single text line",
                     "Treat the image as a single word",
                     "Treat the image as a single word in a circle",
                     "Treat the image as a single character",
                     "Sparse text. Find as much text as possible in no particular order",
                     "Sparse text with OSD",
                     "Raw line. Treat the image as a single text line"
                     ]
        self.segCombo.addItems(seg_modes)
        self.segCombo.setCurrentIndex(self.mainFormHandle.segMode)

        self.segInfoLabel = QLabel()
        self.segInfoLabel.setWordWrap(True)

        self.okBtn = QPushButton("Okay")

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.langLabel)
        self.layout.addLayout(self.anHLayout1)
        self.layout.addWidget(self.addedLangsListWidget)
        self.layout.addLayout(self.anHLayout2)
        self.layout.addWidget(self.addedLangsLabel)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.segLabel)
        self.layout.addWidget(self.segCombo)
        self.layout.addWidget(self.segInfoLabel)
        self.layout.addWidget(self.okBtn, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        self.okBtn.clicked.connect(self.applyChanges)

    def removeSelectedLang(self):
        if self.addedLangsListWidget.count() == 1:
            QMessageBox.information(self, "Info", "At least, you must have one extraction language.")
            return
        self.addedLangsList.remove(self.addedLangsListWidget.currentItem().text())
        self.addedLangsListWidget.takeItem(self.addedLangsListWidget.currentRow())
        self.displayLangs()

    def moveUp(self):
        row = self.addedLangsListWidget.currentRow()
        newRow = row - 1
        item = self.addedLangsListWidget.takeItem(row)
        self.addedLangsListWidget.insertItem(newRow, item)
        luggage = self.addedLangsList[row]
        del self.addedLangsList[row]
        self.addedLangsList.insert(newRow, luggage)

        self.addedLangsListWidget.setCurrentItem(item)

        self.displayLangs()

    def moveDown(self):
        row = self.addedLangsListWidget.currentRow()
        newRow = row + 1
        item = self.addedLangsListWidget.takeItem(row)
        self.addedLangsListWidget.insertItem(newRow, item)
        luggage = self.addedLangsList[row]
        del self.addedLangsList[row]
        self.addedLangsList.insert(newRow, luggage)

        self.addedLangsListWidget.setCurrentItem(item)

        self.displayLangs()

    def displayLangs(self):
        self.addedLangsString = self.addedLangsList[0].split(' ')[0]
        for lang in self.addedLangsList[1:]:
            self.addedLangsString = self.addedLangsString + "+" + lang.split(' ')[0]
        self.addedLangsLabel.setText("Selected Language(s): " + self.addedLangsString)

    def addLangClickedFcn(self):
        text = self.langCombo.currentText()
        if not text in self.addedLangsList:
            self.addedLangsList.append(text)
            self.addedLangsListWidget.addItem(QListWidgetItem(text))
            self.displayLangs()

    def applyChanges(self):
        self.mainFormHandle.selectedLangsList = self.addedLangsList

        self.mainFormHandle.extractionLangIndex = self.langCombo.currentIndex()

        self.mainFormHandle.extractionLangIndex = self.langCombo.currentIndex()
        self.mainFormHandle.segMode = self.segCombo.currentIndex()
        self.mainFormHandle.engineConfigString = "-l {lang} --oem {engineMode} --psm {segMode}" \
            .format(lang=self.addedLangsString, engineMode=1, segMode=self.mainFormHandle.segMode)

        self.close()
