from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QTabWidget, QWidget, QLabel, \
    QMessageBox, QTabBar, QVBoxLayout

import project_resources
from widgets import ImageView


class ViewArea(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.mainFormHandle = parent
        self.threadPool = self.mainFormHandle.threadPool
        self.tmpDirectory = self.mainFormHandle.tmpDirectory

        self.setMinimumSize(1, 1)
        self.setAcceptDrops(True)
        self.currentImageView = None

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(5, 0, 0, 0)

        self.tabWidget = QTabWidget(self)
        self.tabBar = TabBar(self.tabWidget)
        self.tabWidget.setTabBar(self.tabBar)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)

        self.welcomeLabel = QLabel(self)
        self.welcomeLabel.setText(f"""
               <p style="text-align: center;">&nbsp;</p>
               <p style="text-align: center;"><img src={project_resources.AppIcon} width="140" height="140" /></p>
               <p style="text-align: center;"><em>Welcome to <strong>TextChaser</strong></em> ;</p>
               <p style="text-align: center;"><em>to start please open or drag in some image file(s).</em></p>
               <p style="text-align: center;"><em>(you can load up to 30 files at the same time)</em></p>
               <p style="text-align: center;">&nbsp;</p>
               <p style="text-align: center;">&nbsp;</p>
               """)
        self.welcomeFont = QFont("Segoe UI", 11, 2, True)
        self.welcomeLabel.setFont(self.welcomeFont)
        self.welcomeLabel.setWordWrap(True)

        self.vlayout.addWidget(self.tabWidget)
        self.vlayout.addWidget(self.welcomeLabel)
        self.tabWidget.setVisible(False)
        self.welcomeLabel.setVisible(True)

        self.tabWidget.tabCloseRequested.connect(self.handleCloseRequest)
        self.tabWidget.currentChanged.connect(self.currentTabChangeFcn)

    def currentTabChangeFcn(self, idx):
        if self.tabWidget.count() != 0:
            self.currentImageView = self.tabWidget.currentWidget()

            self.mainFormHandle.resetZoomAct.triggered.connect(self.currentImageView.resetZoom)
            self.mainFormHandle.cropAct.triggered.connect(self.currentImageView.cropImage)
            self.mainFormHandle.rotateAct.triggered.connect(self.currentImageView.rotateImage)
            self.mainFormHandle.instantExtractAct.triggered.connect(self.currentImageView.extractSingleBox)
            self.mainFormHandle.resetImageAct.triggered.connect(self.currentImageView.resetImage)
            self.mainFormHandle.grayScaleAct.triggered.connect(self.currentImageView.makeItGray)
            self.mainFormHandle.binarizeAct.triggered.connect(self.currentImageView.makeItBinary)

            self.mainFormHandle.resetZoomAct.setDisabled(False)
            self.mainFormHandle.cropAct.setDisabled(False)
            self.mainFormHandle.rotateAct.setDisabled(False)
            self.mainFormHandle.instantExtractAct.setDisabled(False)
            self.mainFormHandle.colorMenu.setDisabled(False)
            self.mainFormHandle.resetImageAct.setDisabled(False)

        else:
            self.mainFormHandle.resetZoomAct.setDisabled(True)
            self.mainFormHandle.cropAct.setDisabled(True)
            self.mainFormHandle.rotateAct.setDisabled(True)
            self.mainFormHandle.instantExtractAct.setDisabled(True)
            self.mainFormHandle.colorMenu.setDisabled(True)
            self.mainFormHandle.resetImageAct.setDisabled(True)

    def addTab(self, file):
        pixmap = QtGui.QPixmap(file)
        # emit pixmap and file name
        widget = ImageView(parent=self, file=file)
        widget.setPixmapItem(pixmap)
        tab_name = str()
        if len(file) > 15:
            tab_name = "..." + file[-12:]
        self.tabWidget.insertTab(self.tabWidget.currentIndex() + 1, widget, QPixmap(project_resources.TabIcon),
                                 tab_name)
        idx = self.tabWidget.currentIndex()
        self.tabWidget.setCurrentIndex(idx + 1)
        self.tabWidget.setTabToolTip(idx, file)

    def handleCloseRequest(self, index):
        widget = self.tabWidget.widget(index)
        widget.deleteLater()
        self.tabWidget.removeTab(index)
        if self.tabWidget.count() == 0:
            self.tabWidget.setVisible(False)
            self.welcomeLabel.setVisible(True)
        else:
            self.tabWidget.setVisible(True)
            self.welcomeLabel.setVisible(False)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData().hasUrls():
            a0.accept()
        else:
            a0.ignore()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        urlList = a0.mimeData().urls()
        alist = list()
        for url in urlList:
            urlPath = url.toLocalFile()
            if urlPath[-4:] in self.mainFormHandle.sharedData.SupportedFiles:
                alist.append(urlPath)
        if self.tabWidget.count() > 30 or (len(alist) + self.tabWidget.count() > 30):
            QMessageBox.information(self.mainFormHandle, "Info", "You can only have 30 files open at the same time.")
            return

        elif len(alist) != 0:
            self.mainFormHandle.showImages(alist)

        else:
            a0.ignore()

    def closeAllTabs(self):
        tab_count = self.tabWidget.count()
        if tab_count == 0:
            QMessageBox.information(self, "Info", "There is no open tab.")
            return
        qassert = QMessageBox.question(self, "Assertion", "Are you sure you want to close all tabs?",
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if qassert == QMessageBox.Yes:
            for idx in range(self.tabWidget.count()):
                self.tabWidget.tabCloseRequested.emit(0)


class TabBar(QTabBar):
    def __init__(self, parent=None):
        QTabBar.__init__(self, parent)

        self.setIconSize(QtCore.QSize(25, 25))

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.MouseButton.MiddleButton:
            self.tabCloseRequested.emit(self.tabAt(a0.pos()))
        super(QTabBar, self).mouseReleaseEvent(a0)
