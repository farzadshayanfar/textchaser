import os

from PySide6.QtCore import QDir, QStandardPaths, Qt
from PySide6.QtWidgets import QTreeView, QFileSystemModel, QMessageBox

from widgets import Worker


class FileBrowser(QTreeView):
    def __init__(self, parent=None):
        QTreeView.__init__(self, parent)
        self.mainFormHandle = parent
        self.threadPool = self.mainFormHandle.threadPool

        self.setMinimumSize(1, 1)
        self.model = QFileSystemModel()
        rootPath = QDir.rootPath()
        self.model.setRootPath(rootPath)
        self.model.setOption(QFileSystemModel.DontUseCustomDirectoryIcons)
        self.setModel(self.model)
        desktopLocation = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        desktopIdx = self.model.index(desktopLocation)
        self.expandPath(desktopIdx)
        self.setUniformRowHeights(True)
        self.setIndentation(20)
        for colidx in range(1, 4):
            self.hideColumn(colidx)
        self.header().hide()
        self.setColumnWidth(0, 500)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setDragEnabled(True)
        self.horizontalScrollBar().setEnabled(True)
        self.setExpandsOnDoubleClick(True)

        self.doubleClicked.connect(self.handleDblClick)

    def openFiles(self, index):
        fileName = self.model.filePath(index)
        if os.path.isdir(fileName) or fileName[-4:] not in (".jpg", ".png", ".tif", ".bmp", "jpeg"):
            return
        else:
            viewer = self.mainFormHandle.Viewer
            if viewer.tabWidget.count() > 30 or (1 + viewer.tabWidget.count() > 30):
                QMessageBox.information(self.mainFormHandle, "Info",
                                        "You can only have 30 files open at the same time.")
                return
            self.mainFormHandle.showImages(fileName)

    def handleDblClick(self, index):
        worker = Worker.Worker(self.openFiles, index)
        self.threadPool.start(worker)

    def expandPath(self, index):
        if not index.isValid():
            return
        indexes = []
        ix = index
        while ix.isValid():
            indexes.insert(0, ix)
            ix = ix.parent()
        for ix in indexes:
            self.expand(ix)
