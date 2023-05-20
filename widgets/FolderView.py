import glob
import os
import tempfile

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QCloseEvent, QContextMenuEvent, QAction
from PySide6.QtWidgets import QMainWindow, QToolBar, QListWidget, QFrame, QHBoxLayout, QSplitter, \
    QApplication, QLabel, QStatusBar, QFileDialog, QListWidgetItem, QMenu, QAbstractItemView

from widgets import Worker, ProgressBar, FolderViewViewer, StatusLabel


class FolderView(QMainWindow):
    extractTextFromDocsSig = Signal(str, int)
    advanceProgressSig = Signal(int, int)
    updateStatusLabelSig = Signal(str)

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.mainFormHandle = parent
        self.threadPool = self.mainFormHandle.threadPool
        self.tmpDirectory = tempfile.TemporaryDirectory()
        self.guestTempDir = tempfile.TemporaryDirectory()

        self.setWindowTitle("Folder View Form")
        self.setWindowIcon(QIcon("res/icons/folderView.png"))
        self.resize(820, 700)

        self.settingsAct = QAction("Folder view settings")
        self.settingsAct.setIcon(QIcon("res/icons/viewerSettings.png"))

        self.openFolderAct = QAction("Open a folder image content")
        self.openFolderAct.setIcon(QIcon("res/icons/folderView.png"))
        self.openFolderAct.triggered.connect(self.openFolder)
        self.openFolderAct.setStatusTip("Open all images from a folder")

        self.stopAct = QAction("Stop batch process")
        self.stopAct.setIcon(QIcon("res/icons/stop.svg"))
        self.stopAct.triggered.connect(self.stop)
        self.stopAct.setStatusTip("Stop the process")
        self.StopProcess = False

        self.startAct = QAction("Start batch process")
        self.startAct.setIcon(QIcon("res/icons/startFV.svg"))
        self.startAct.triggered.connect(self.start)
        self.startAct.setStatusTip("Start processing")

        self.cWidget = QFrame(self)
        self.setCentralWidget(self.cWidget)
        self.cLayout = QHBoxLayout(self.cWidget)
        self.cLayout.setContentsMargins(0, 0, 0, 0)

        self.noticeLabel = QLabel(self.cWidget)
        self.noticeLabel.setText("""
        <p style="text-align: center;">&nbsp;<img src="res/icons/folderView.svg" width="110" height="100" /></p>
        <p style="text-align: center;"><em>This is the <strong>Folder View Form</strong></em>&nbsp;;</p>
        <p style="text-align: center;"><em>in this window you can open the contents of </em></p>
        <p style="text-align: center;"><em>a folder, order,&nbsp;</em><em>pre process, and process all images</em></p>
        <p style="text-align: center;"><em> at the same time. This</em><em> form is for batch processing</em></p>
        <p style="text-align: center;"><em> of a lot of images located in one&nbsp;</em><em>folder.</em></p>
        """)
        self.noticeLabel.setWordWrap(True)

        self.imageListWidget = ImageListWidget(parent=self)

        self.viewer = FolderViewViewer.FolderViewViewer(parent=self)

        self.aSplitter = QSplitter(self.cWidget)
        self.aSplitter.setVisible(False)
        self.aSplitter.setOrientation(Qt.Horizontal)
        self.aSplitter.addWidget(self.imageListWidget)
        self.aSplitter.addWidget(self.viewer)
        self.aSplitter.setSizes([200, 600])
        self.cLayout.addWidget(self.noticeLabel)
        self.cLayout.addWidget(self.aSplitter)

        self.toolbar = QToolBar("Folder View Toolbar")
        self.toolbar.setIconSize(QSize(27, 27))
        self.toolbar.setStyleSheet("""
        QToolBar {
        margin: 5px 0px 5px 2px;
        padding: 2px 0px 2px 2px;
        spacing: 3px;
        border: 0px;
        }
        """)

        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addActions([self.settingsAct, self.openFolderAct, self.imageListWidget.clearAllAct])
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.imageListWidget.editFileNameAct,
                                 self.imageListWidget.removeSelectedAct,
                                 self.imageListWidget.checkAllAct,
                                 self.imageListWidget.uncheckAllAct,
                                 self.imageListWidget.checkAct,
                                 self.imageListWidget.uncheckAct])

        self.toolbar.addSeparator()
        self.toolbar.addActions([self.viewer.panAct, self.viewer.zoomInAct, self.viewer.zoomOutAct,
                                 self.viewer.resetZoomAct, self.viewer.cropAct, self.viewer.instantExtractAct,
                                 self.viewer.rotateAct, self.viewer.binarizeAct, self.viewer.grayScaleAct,
                                 self.viewer.resetImageAct])
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.stopAct, self.startAct])

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbarLabel = QLabel()
        self.statusbarLabel.setVisible(False)
        self.progressbar = ProgressBar.ProgressBar(parent=self)
        self.progressbar.setVisible(False)
        self.statusCountLabel = StatusLabel.StatusLabel(parent=self)
        self.statusCountLabel.setText("#: 0")
        self.statusbar.addPermanentWidget(self.statusbarLabel)
        self.statusbar.addPermanentWidget(self.progressbar)
        self.statusbar.addPermanentWidget(self.statusCountLabel)

        self.imageListWidget.currentItemChanged.connect(self.handleChange)

        self.extractTextFromDocsSig.connect(self.mainFormHandle.extractTextFromDocs)
        self.advanceProgressSig.connect(self.progressbar.advance)
        self.updateStatusLabelSig.connect(self.updateStatusLabel)

    def openFolder(self, folder_path=None):
        if not folder_path:
            file_dialog = QFileDialog()
            folder_path = file_dialog.getExistingDirectory()
            folder_path = os.path.abspath(folder_path)

        worker = Worker.Worker(self.doOpenFolder, folder_path)
        self.threadPool.start(worker)

    def doOpenFolder(self, folder_name):
        pngs = glob.glob(os.path.join(folder_name, "*.png"))
        jpgs = glob.glob(os.path.join(folder_name, "*.jpg"))
        tifs = glob.glob(os.path.join(folder_name, "*.tif"))
        bmps = glob.glob(os.path.join(folder_name, "*.bmp"))
        images_paths = pngs + jpgs + tifs + bmps

        if images_paths:
            self.aSplitter.setVisible(True)
            self.noticeLabel.setVisible(False)
            for path in images_paths:
                item = FolderViewItem(filePath=path)
                item.setText(path.split(sep="\\")[-1])
                self.imageListWidget.addItem(item)

        self.updateCountLabel()

    def updateCountLabel(self):
        self.statusCountLabel.setText("#: " + str(self.imageListWidget.count()))

    def updateStatusLabel(self, text):
        self.statusbarLabel.setText(text)

    def stop(self):
        self.StopProcess = True

    def start(self):
        worker = Worker.Worker(self.dostart)
        self.threadPool.start(worker)

    def dostart(self):
        item_count = self.imageListWidget.count()
        if not item_count:
            return

        checked_item_list = list()

        for idx in range(item_count):
            item = self.imageListWidget.item(idx)
            if item.checkState() == Qt.Checked:
                checked_item_list.append(item)
        if not checked_item_list:
            return

        self.startAct.setDisabled(True)
        self.statusbarLabel.setVisible(True)
        self.progressbar.reset()
        self.progressbar.setVisible(True)
        step = self.progressbar.getStep(len(checked_item_list))

        for item in checked_item_list:
            if not self.StopProcess:
                self.advanceProgressSig.emit(step, 0)
                self.updateStatusLabelSig.emit(item.originalPath())
                self.mainFormHandle.extractTextFromDocs(item.currentPath(), 0)
            else:
                self.StopProcess = False
                break

        self.startAct.setDisabled(False)
        self.statusbarLabel.setVisible(False)
        self.progressbar.setVisible(False)

    def handleChange(self, item):
        try:
            self.statusbar.showMessage(item.originalPath())
            self.viewer.loadItemImage(item)
        except AttributeError:
            pass

    def closeEvent(self, event: QCloseEvent):
        self.setVisible(False)


class ImageListWidget(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)

        self.FolderViewHandle = parent

        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

        # region context menu
        self.editFileNameAct = QAction("Edit file name")
        self.editFileNameAct.setIcon(QIcon("res/icons/edit.svg"))
        self.editFileNameAct.triggered.connect(self.editFileName)
        self.editFileNameAct.setStatusTip("Rename the selected file name")

        self.removeSelectedAct = QAction("Remove from list")
        self.removeSelectedAct.setIcon(QIcon("res/icons/remove.svg"))
        self.removeSelectedAct.triggered.connect(self.removeSelected)
        self.removeSelectedAct.setStatusTip("Remove the selected item from the list")

        self.checkAllAct = QAction("Check all images for processing")
        self.checkAllAct.setIcon(QIcon("res/icons/checkAll.svg"))
        self.checkAllAct.triggered.connect(self.checkAllItems)
        self.checkAllAct.setStatusTip("Check all items on the list to be processed")

        self.uncheckAllAct = QAction("Uncheck all images")
        self.uncheckAllAct.setIcon(QIcon("res/icons/uncheckAll.svg"))
        self.uncheckAllAct.triggered.connect(self.uncheckAllItems)
        self.uncheckAllAct.setStatusTip("Uncheck all items on the list")

        self.checkAct = QAction("Select")
        self.checkAct.setIcon(QIcon("res/icons/check.svg"))
        self.checkAct.triggered.connect(self.checkItem)
        self.checkAct.setStatusTip("Check the selected item")

        self.uncheckAct = QAction("Deselect")
        self.uncheckAct.setIcon(QIcon("res/icons/uncheck.svg"))
        self.uncheckAct.triggered.connect(self.uncheckItem)
        self.uncheckAct.setStatusTip("Uncheck the selected item")

        self.clearAllAct = QAction("Clear the list")
        self.clearAllAct.setIcon(QIcon("res/icons/clear.svg"))
        self.clearAllAct.triggered.connect(self.clearAll)
        self.clearAllAct.setStatusTip("Clear all items from the list")

        self.contexMenu = QMenu()
        self.contexMenu.addActions([self.editFileNameAct, self.removeSelectedAct, self.checkAct,
                                    self.clearAllAct, self.uncheckAct, self.checkAllAct])
        # endregion context menu

    def checkAllItems(self):
        worker = Worker.Worker(self.doCheckAllItems)
        self.FolderViewHandle.threadPool.start(worker)

    def doCheckAllItems(self):
        for idx in range(self.count()):
            self.item(idx).setCheckState(Qt.Checked)

    def uncheckAllItems(self):
        worker = Worker.Worker(self.doUncheckAllItems)
        self.FolderViewHandle.threadPool.start(worker)

    def doUncheckAllItems(self):
        for idx in range(self.count()):
            self.item(idx).setCheckState(Qt.Unchecked)

    def checkItem(self):
        self.currentItem().setCheckState(Qt.Checked)

    def uncheckItem(self):
        self.currentItem().setCheckState(Qt.Unchecked)

    def editFileName(self):
        index = self.currentIndex()
        self.edit(index)

    def removeSelected(self):
        current_row = self.currentRow()
        self.takeItem(current_row)
        self.checkCount()
        self.FolderViewHandle.updateCountLabel()

    def clearAll(self):
        self.FolderViewHandle.viewer.clear()
        self.FolderViewHandle.statusbar.clearMessage()
        self.clear()
        self.checkCount()
        self.FolderViewHandle.updateCountLabel()

    def contextMenuEvent(self, arg__1: QContextMenuEvent):
        self.contexMenu.exec_(arg__1.globalPos())

    def checkCount(self):
        if not self.count():
            self.FolderViewHandle.aSplitter.setVisible(False)
            self.FolderViewHandle.noticeLabel.setVisible(True)


class FolderViewItem(QListWidgetItem):
    def __init__(self, filePath):
        QListWidgetItem.__init__(self)

        self.setFlags(self.flags() | Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
        self.setCheckState(Qt.Unchecked)
        self._originalPath = filePath
        self._currentPath = filePath

    def originalPath(self):
        return self._originalPath

    def setCurrentPath(self, path):
        self._currentPath = path

    def currentPath(self):
        return self._currentPath


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    form = FolderView()
    form.show()
    app.exec_()
