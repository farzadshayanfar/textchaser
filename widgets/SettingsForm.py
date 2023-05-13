from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication, QListWidget, QHBoxLayout, QSplitter, QVBoxLayout, \
    QPushButton, QSpacerItem, QSizePolicy


class SettingsForm(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.mainFormHandle = parent
        self.setWindowTitle("Settings")
        self.setWindowIcon(self.mainFormHandle.sharedData.appIcon)
        self.initUI()

    def initUI(self):
        self.setVisible(False)
        self.W = 400
        self.H = 500
        desktop = QApplication.desktop()
        screenWidth = desktop.width()
        screenHeight = desktop.height()
        x = int((screenWidth - self.W) / 2)
        y = int((screenHeight - self.H) / 2)
        self.move(x, y)

        self.baseWidget = QWidget()

        self.appearance = QWidget()
        self.appearanceSizes = list()
        self.engines = QWidget()
        self.enginesSizes = list()

        self.sectionDict = dict()
        self.sectionDict["Appearance"] = self.appearance
        self.sectionDict["Engines"] = self.engines

        self.sectionList = QListWidget()
        for entry in self.sectionDict.keys():
            self.sectionList.addItem(entry)
        self.sectionList.currentItemChanged.connect(self.showSelectedSection)

        self.restoreDefaults = QPushButton("Restore Defaults")
        self.closeSettings = QPushButton("Close Settings")
        self.closeSettings.clicked.connect(self.closeEvent)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.addWidget(self.sectionList)
        self.splitter.addWidget(self.baseWidget)
        self.splitter.setSizes([200, 200])

        self.hLayout = QHBoxLayout()
        self.hLayout.addSpacerItem(QSpacerItem(160, 10, hPolicy=QSizePolicy.Expanding))
        self.hLayout.addWidget(self.restoreDefaults)
        self.hLayout.addWidget(self.closeSettings)

        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.splitter)
        self.vLayout.addLayout(self.hLayout)

        self.baseWidgetLayout = QHBoxLayout(self.baseWidget)
        for widget in self.sectionDict.values():
            self.baseWidgetLayout.addWidget(widget)
            widget.setVisible(False)
        self.appearance.setVisible(True)

    def showSelectedSection(self):
        widgetName = self.sectionList.currentItem().text()
        widget = self.sectionDict[widgetName]
        for widget in self.sectionDict.values():
            widget.setVisible(False)
        widget.setVisible(True)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.setVisible(False)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    s = SettingsForm()
    s.show()
    app.exec_()
