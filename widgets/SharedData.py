import os

from PySide6 import QtGui, QtCore


class SharedData(object):
    def __init__(self, mainFormHandle=None):
        self.mainFormHandle = mainFormHandle
        aQDir = QtCore.QDir().filePath("res/icons/TextChaser.png")
        aQDir2 = QtCore.QDir().filePath("res/icons/TextChaser2.png")
        self.appIconAdd = os.path.abspath(aQDir)
        self.appIconAdd2 = os.path.abspath(aQDir2)
        self.appIcon = QtGui.QIcon(self.appIconAdd)
        self.appIcon2 = QtGui.QIcon(self.appIconAdd2)
        self.imgIcon = QtGui.QIcon(("res/icons/image.png"))
        self.currentFile = str()
        self.recentOpenFiles = list()
        self.SupportedFiles = (".jpg", ".png", ".tif", ".bmp", "jpeg")
        self.configDict = {"recentOpenFileNames": self.recentOpenFiles}
